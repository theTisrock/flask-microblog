# begin translate

import requests, json
from microblog_app import app
from flask_babel import _


def translate(text, source_language, destination_language):
    """
    :param text: comes from Javascript ajax request from client
    :param source_language: from
    :param destination_language: to
    :return:
    """

    # check configuration
    if 'MS_TRANSLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
        return _("The translation service is not configured.")
    # configuration okay, hit the API

    # assemble uri
    url = "https://api.microsofttranslator.com/Ajax.svc/Translate?"
    parameters = f"text={text}&from={source_language}&to={destination_language}"  # uniform resource name
    uri = url + parameters

    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}  # obtain authorization

    response = requests.get(uri, headers=auth)  # send request & capture response

    if response.status_code != 200:
        return "There was a problem with the translation."
    # return the translated text to the client's asynchronous javascript request
    return json.loads(response.content.decode('utf-8-sig'))

# end translate.py
