from flask import Flask, request, jsonify
from data_utils import load_sentencepiece_model
from utils import create_masks
from model import Transformer, Encoder, Decoder
import tensorflow_text as tf_text
import tensorflow as tf
import numpy as np
import json

app = Flask(__name__)


@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data['text']

    # Call the provided Python function to translate the text
    # into Shakespearean English
    translated_text = translate_to_shakespearean(text)

    response = {
        'translated_text': translated_text
    }
    return jsonify(response)


def translate_to_shakespearean(text):
    # Load the necessary models
    inp_tokenizer, tar_tokenizer = load_tokenizers()
    model, configs = load_model()

    # Translate the text into Shakespearean English
    output, _ = eager_single_predict(text, inp_tokenizer, model)
    output_text = tf_text.detokenize(output)[0].numpy(
    ).decode().replace('<sos>', '').replace('<eos>', '')

    return output_text


if __name__ == '__main__':
    app.run(port=5000)
