import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main() -> None:
    """Print a message to the console."""
    click.echo(message="Hello world!")
