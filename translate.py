from google.cloud import translate_v2 as translate
import json
import os
import six
import html

with open('config/config.json') as json_file:
    config = json.load(json_file)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=config["G_CLOUD_SERVICE_KEYFILE"]


def google_translate(text, language="en"):
    """
    Translates text into the target language
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=language)
    result['translatedText'] = html.unescape(result['translatedText']) #
    return result
