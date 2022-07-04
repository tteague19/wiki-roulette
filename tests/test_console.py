import click.testing
import pytest

from wiki_roulette import console


@pytest.fixture()
def runner() -> click.testing.CliRunner:
    """Create an object to invoke the CLI."""
    return click.testing.CliRunner()


def test_main_succeeds(runner: click.testing.CliRunner) -> None:
    """
    Test whether the main() function of console.py succeeds.

    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    # An exit code of zero indicates the program was successful.
    assert result.exit_code == 0
