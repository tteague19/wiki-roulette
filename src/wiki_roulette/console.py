"""Provide a command-line interface to get a random article from Wikipedia."""
import locale
import textwrap
from typing import Optional

import click

from wiki_roulette import __version__, wikipedia


def extract_locale_language_code(split_char: Optional[str] = "_") -> str:
    """
    Obtain the language code associated with the machine's location.

    :param split_char: The character that separates the ISO 639-1 language
        code from appended specifiers, defaults to "_"
    :type split_char: str, optional
    :return: The language code of the current machine
    :rtype: str

    .. doctest::
        >>> lang_code = extract_locale_language_code(split_char="_")
        >>> lang_code == "en"
        True
    """
    language_code, _ = locale.getdefaultlocale()
    return str(language_code).split(split_char)[0]


@click.command()
@click.option(
    "-l",
    "--language",
    "language",
    help="Language edition of Wikipedia",
    metavar="LANG",
    default=extract_locale_language_code(),
    show_default=True,
)
@click.version_option(version=__version__)
def main(language: str) -> None:
    """
    Print a random Wikipedia article to the console.

    :param language: The ISO 639-1 language code of the language version of
        Wikipedia from which to get an article
    """
    data = wikipedia.obtain_random_page(language=language)

    click.secho(message=data.title, fg="green")

    # The use of textwrap wraps the text so that every line is at most 70
    # characters long.
    click.echo(message=textwrap.fill(text=data.extract))
