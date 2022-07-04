import click.testing

from wiki_roulette import console


def test_main_succeeds() -> None:
    """Test whether the main() function of console.py succeeds."""
    runner = click.testing.CliRunner()
    result = runner.invoke(cli=console.main)

    # An exit code of zero indicates the program was successful.
    assert result.exit_code == 0
