from data_utils import load_sentencepiece_model
from utils import create_masks
from model import Transformer, Encoder, Decoder
import matplotlib.pyplot as plt
import tensorflow_text as tf_text
import tensorflow as tf
import numpy as np
import json
from difflib import SequenceMatcher


def load_model(filename='../trained_models/model_config.json'):
    # Load model configuration
    with open(filename, 'r') as file:
        configs = json.loads(file.read())

    # Load the model from weights
    model = Transformer(**configs)
    inp = tf.random.uniform((1, 4), 0, 10, tf.int32)
    _ = model(inp, inp, False, None, None, None)
    model.load_weights('../trained_models/translator_weights')
    return model, configs


def load_tokenizers(inp_file='../tokenizers/modern2k.model',
                    tar_file='../tokenizers/original2k.model'):
    inp_tokenizer = load_sentencepiece_model(inp_file, 1)
    tar_tokenizer = load_sentencepiece_model(tar_file, 1)
    return inp_tokenizer, tar_tokenizer


def plot_attn_weights(inp_text, tar_seq, attn_weights, inp_tokenizer, tar_tokenizer):
    fig = plt.figure(figsize=(8, 8))

    inp_seq = inp_tokenizer.tokenize(inp_text)
    tar_seq = tf.squeeze(tar_seq, 0)
    inp_seq = [x.numpy().decode() for x in inp_tokenizer.id_to_string(inp_seq)]
    tar_seq = [x.numpy().decode() for x in tar_tokenizer.id_to_string(tar_seq)]
    attn_weights = tf.squeeze(attn_weights, 0)

    for head in range(attn_weights.shape[0]):
        ax = fig.add_subplot(2, 2, head+1)
        ax.matshow(attn_weights[head], cmap='viridis')
        fontdict = {'fontsize': 14}
        ax.set_xticks(range(len(inp_seq)+2))
        ax.set_yticks(range(len(tar_seq)))
        ax.set_xticklabels(['<sos>']+inp_seq+['<eos>'], fontdict=fontdict,
                           rotation=45)
        ax.set_yticklabels(tar_seq[1:]+['<eos>'], fontdict=fontdict)
        ax.set_xlabel('Head {}'.format(head+1))

    plt.tight_layout()
#     plt.savefig('insult')
    plt.show()


def eager_single_predict(input_sentence, inp_tokenizer, model,
                         temp=1., max_length=100):
    inp = tf.concat([[1], inp_tokenizer.tokenize(
        input_sentence), [2]], 0)[tf.newaxis, :]
    tar = tf.constant([1], dtype=inp.dtype)[tf.newaxis, :]
    for i in range(max_length):
        enc_mask, comb_mask, dec_mask = create_masks(inp, tar)
        preds, weights = model(inp, tar, training=False, enc_padding_mask=enc_mask,
                               look_ahead_mask=comb_mask, dec_padding_mask=dec_mask)
        next_token = tf.cast(tf.random.categorical(
            preds[:, -1]/temp, 1), tar.dtype)
        if tf.reduce_all(tf.equal(next_token, 2)):
            break
        tar = tf.concat([tar, next_token], axis=1)
    return tar, weights


def eager_beam_search(input_text, inp_tokenizer, model, K=5, maxlen=32):
    x = tf.concat([[1], inp_tokenizer.tokenize(input_text), [2]], 0)
    x = tf.repeat(x[tf.newaxis, :], K, axis=0)
    y = tf.ones((K, 1), dtype=x.dtype)
#     y = tf.concat([y, tf.zeros((K, MAX_LENGTH-1), dtype=inp.dtype)], 1)
    flattened_row_ids = tf.repeat(tf.range(K), K)
    # mask out the lower entries to start
    prior = tf.constant([0.]+[-1e5]*(K-1))
    eos_mask = tf.zeros((K, 1), dtype=tf.float32)
    new_tokens = tf.constant([[0]])

    for i in range(maxlen):
        if tf.not_equal(new_tokens[0], 2):
            logits, _ = model(x, y, False, None, None, None)
            log_probs = tf.nn.log_softmax(logits[:, -1, :])
            log_probs += tf.reshape(prior, (-1, 1))
            log_probs += eos_mask

            prob_matrix, token_matrix = tf.math.top_k(log_probs, k=K)
            prob_list = tf.reshape(prob_matrix, (1, -1))
            token_list = tf.reshape(token_matrix, (1, -1))

            prior, list_ids = tf.math.top_k(prob_list, k=K)
            row_id = tf.gather(flattened_row_ids, tf.squeeze(list_ids))
            new_tokens = tf.gather(token_list[0], list_ids[0])
            eos_mask = -1e5*tf.reshape(
                tf.cast(tf.equal(new_tokens, 2), tf.float32), (-1, 1))

            y = tf.gather(y, row_id)
            y = tf.concat([y, new_tokens[:, tf.newaxis]], axis=1)
#             y = tf.concat([y[:,:i+1], new_tokens[:,tf.newaxis], y[:,i+2:]], axis=1)
        else:
            break
    return y, prior[0]


def batch_random_predict(input_text, inp_tokenizer, model,
                         temp=1.0, n_samples=16, max_length=16):

    inp = tf.concat([[1], inp_tokenizer.tokenize(input_text), [2]], 0)
    inp = tf.repeat(inp[tf.newaxis, :], n_samples, axis=0)

    tar = tf.ones((n_samples, 1), dtype=inp.dtype)
    mask = tf.ones((n_samples, 1), dtype=tf.bool)  # for ended sentences

    for _ in range(max_length):
        enc_mask, comb_mask, dec_mask = create_masks(inp, tar)
        logits, weights = model(inp, tar, training=False,
                                enc_padding_mask=enc_mask,
                                look_ahead_mask=comb_mask,
                                dec_padding_mask=dec_mask)

        logits = logits[:, -1, :]/tf.cast(temp, tf.float32)
        next_tokens = tf.cast(tf.random.categorical(logits, 1), inp.dtype)

        # replace any already finished sentences with padding 4 next token
        next_tokens = tf.where(mask, next_tokens, 0)

        # update mask. to stay true, it must:
        # 1) already be true
        # 2) not currently be an end of sentence token
        mask = tf.logical_and(mask, tf.not_equal(next_tokens, 2))
        tar = tf.concat([tar, next_tokens], axis=1)
        if not tf.reduce_any(mask):
            break
    return tar, weights


def sort_by_most_similar(arr):
    """ For each row, it computes the mean similarity score with all other
    rows and stores it in sims. Then it chooses the row with highest mean
    and returns the array at that index."""
    sims = []
    if tf.is_tensor(arr):
        arr = arr.numpy()
    N = arr.shape[0]
    for i in range(N):
        sims.append(-np.mean([SequenceMatcher(a=arr[i], b=arr[j]).ratio()
                              for j in range(N) if j != i]))
    return np.argsort(sims)


def minimum_bayes_risk_predict(input_text, inp_tokenizer, model,
                               temp=1.0, n_samples=16, max_length=16):
    translations, weights = batch_random_predict(input_text, inp_tokenizer, model,
                                                 temp, n_samples, max_length)
    if tf.is_tensor(translations):
        translations = translations.numpy()
    permuatation = sort_by_most_similar(translations)
    translations = translations[permuatation]
    weights = {k: tf.gather(v, permuatation) for k, v in weights.items()}
    return translations, weights


def get_beam_preds(text, inp_tokenizer, tar_tokenizer, model):
    translations, probs = eager_beam_search(text, inp_tokenizer, model)
    for sent, prob in zip(translations, probs):
        sent = tar_tokenizer.detokenize(sent).numpy().decode()
        return sent


if __name__ == "__main__":
    model, configs = load_model()
    inp_tokenizer, tar_tokenizer = load_tokenizers()
