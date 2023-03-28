from flask import Flask, request, jsonify
from translator import get_beam_preds, load_model, load_tokenizers

app = Flask(__name__)

model, configs = load_model()
inp_tokenizer, tar_tokenizer = load_tokenizers()


@app.route('/translate', methods=['POST'])
def translate():
    if request.json['button'] == 'Shakespherify':
        text = request.json['text']
        translation = get_beam_preds(text, inp_tokenizer, tar_tokenizer, model)
        return jsonify({'translation': translation})
    else:
        return jsonify({'translation': request.json['text']})


if __name__ == '__main__':
    app.run()
