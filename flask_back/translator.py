import requests
import json


def translate_to_shakespeare(text):
    endpoint = "https://api.funtranslations.com/translate/shakespeare.json"
    response = requests.post(endpoint, data={"text": text})
    if response.status_code != 200:
        raise Exception("Translation failed")
    translated_text = json.loads(
        response.content.decode('utf-8'))['contents']['translated']
    return translated_text
