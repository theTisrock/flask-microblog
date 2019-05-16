# begin translate

import requests, json
from microblog_app import app
# from flask_babel import _


def translate(text, source_language, destination_language):
    """
    This function is the workhorse for the top level request in routes.
    It makes a subsequent request to a third party and returns the results.

    :param text: comes from Javascript ajax request from client
    :param source_language: from
    :param destination_language: to
    :return:
    """

    # check configuration
    if 'MS_TRANSLATOR_KEY' not in app.config or not app.config['MS_TRANSLATOR_KEY']:
        return "The translation service is not configured."
    # configuration okay, hit the API

    # assemble uri
    url = "https://api.microsofttranslator.com/Ajax.svc/Translate?"
    parameters = f"text={text}&from={source_language}&to={destination_language}"  # uniform resource name
    uri = url + parameters

    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}  # obtain authorization

    response = requests.get(uri, headers=auth)  # send request & capture response

    if response.status_code != 200:

        error_message = "Failed Translation "
        bill_gates = "\nBill Gates wants a 2nd Porsche 959. Donate to the cause!"

        if response.status_code == 403:
            error_message += f"{response.status_code}: Out of call volume quota." + bill_gates
        elif response.status_code == 429:
            error_message += f"{response.status_code}: Rate limit exceeded." + bill_gates
        else:
            error_message += "There was an error with the 3rd party API request."
        return error_message

    return json.loads(response.content.decode('utf-8-sig'))  # return the translated text

# end translate.py
