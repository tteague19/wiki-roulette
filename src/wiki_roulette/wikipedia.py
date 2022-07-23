"""Client for the Wikipedia REST API, version 1."""
from dataclasses import dataclass, field

import click
import desert
import marshmallow
import requests

# This URL is the REST API of Wikipedia that returns the summary of
# a random article from Wikipedia. We leave the country code blank to enable
# a user to specify the language.
API_URL_TEMPLATE: str = "/".join(
    ["https://{language}.wikipedia.org", "api", "rest_v1", "page", "random", "summary"]
)


@dataclass()
class WikipediaPage:
    """
    Data class to represent the title and summary of a Wikipedia page.

    :param title: The title of the article on a Wikipedia page
    :type title: str
    :param extract: The opening paragraph of the article on a Wikipedia page
    :type extract: str
    """

    title: str = field(metadata=desert.metadata(field=marshmallow.fields.String()))
    extract: str = field(metadata=desert.metadata(field=marshmallow.fields.String()))


schema = desert.schema(cls=WikipediaPage, meta={"unknown": marshmallow.EXCLUDE})


def obtain_random_page(language: str) -> WikipediaPage:
    """
    Obtain a random page from Wikipedia.

    This function performs a GET request to the /page/random/summary endpoint
    Wikipedia hosts.

    :param language: The language version of Wikipedia to use in the form of
        an ISO 639-1 or ISO 639-3 code
    :type language: str
    :return: The response from the Wikipedia random article API
    :rtype: WikipediaPage
    :raises ClickException: Raise an exception if we provide an invalid
        schema or encounter an error in the GET request
    """
    url = API_URL_TEMPLATE.format(language=language)

    try:
        with requests.get(url=url) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data=data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message=message) from error
