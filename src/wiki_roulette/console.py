import textwrap

import click
import requests

from . import __version__

# This URL is the REST API of the English Wikipedia that returns the summary of
# a random article from Wikipedia.
API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Print a random Wikipedia article to the console."""
    try:
        with requests.get(API_URL) as response:
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
            message=f"The Wikipedia API at {API_URL} is unreachable.",
            fg="red")
