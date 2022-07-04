import locale
import textwrap

import click
import requests

from src.wiki_roulette import __version__

# This URL is the REST API of Wikipedia that returns the summary of
# a random article from Wikipedia. We leave the country code blank to enable
# a user to specify the language.
API_URL_TEMPLATE = "/".join(
    [
        "https://{language}.wikipedia.org",
        "api",
        "rest_v1",
        "page",
        "random",
        "summary"
    ]
)


def extract_locale_language_code(split_char: str = "_") -> str:
    """
    Obtain the language code associated with the machine's location.

    :param split_char: The character that separates the ISO 639-1 language
        code from appended specifiers, defaults to "_"
    :type split_char: str, optional
    :return: The language code of the current machine
    :rtype: str
    """
    language_code, _ = locale.getdefaultlocale()
    return language_code.split(split_char)[0]


@click.command()
@click.option(
    "-l",
    "--language",
    "language",
    default=extract_locale_language_code(),
    show_default=True)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """
    Print a random Wikipedia article to the console.

    :param language: The ISO 639-1 language code of the language version of
        Wikipedia from which to get an article
    :type language: str
    """
    url = API_URL_TEMPLATE.format(language=language)
    with requests.get(url=url) as response:
        response.raise_for_status()
        data = response.json()

    title = data["title"]
    extract = data["extract"]

    click.secho(message=title, fg="green")

    # The use of textwrap wraps the text so that every line is at most 70
    # characters long.
    click.echo(message=textwrap.fill(text=extract))
