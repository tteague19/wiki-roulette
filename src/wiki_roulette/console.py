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


@click.command()
@click.option("-l", "--language", "language", default="en", show_default=True)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """
    Print a random Wikipedia article to the console.

    :param language: The ISO 639-1 language code of the language version of
        Wikipedia from which to get an article
    :type language: str
    """
    url = API_URL_TEMPLATE.format(language=language)
    try:
        with requests.get(url=url) as response:
            response.raise_for_status()
            data = response.json()

        title = data["title"]
        extract = data["extract"]

        click.secho(message=title, fg="green")

        # The use of textwrap wraps the text so that every line is at most 70
        # characters long.
        click.echo(message=textwrap.fill(text=extract))

    except requests.HTTPError:
        click.secho(
            message=f"The Wikipedia API at {url} is unreachable.",
            fg="red")

    except requests.ConnectionError:
        click.secho(
            message=f"Unable to connect to {url}.",
            fg="red")
