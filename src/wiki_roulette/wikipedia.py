from typing import Any

import click
import requests

# This URL is the REST API of Wikipedia that returns the summary of
# a random article from Wikipedia. We leave the country code blank to enable
# a user to specify the language.
API_URL_TEMPLATE = "/".join(
    ["https://{language}.wikipedia.org", "api", "rest_v1", "page", "random", "summary"]
)


def obtain_random_page(language: str) -> Any:
    """
    Obtain a random page from Wikipedia.

    :param language: The language version of Wikipedia to use in the form of
        an ISO 639-1 or ISO 639-3 code
    :type language: str
    :return: The response from the Wikipedia random article API
    :rtype: Any
    """
    url = API_URL_TEMPLATE.format(language=language)

    try:
        with requests.get(url=url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message=message) from error
