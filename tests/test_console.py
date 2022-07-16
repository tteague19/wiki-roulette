import unittest.mock

import click.testing
import pytest
import requests
from pytest_mock import MockFixture

from wiki_roulette import console


@pytest.fixture()
def runner() -> click.testing.CliRunner:
    """Create an object to invoke the CLI."""
    return click.testing.CliRunner()


@pytest.fixture()
def mock_wikipedia_random_page(
    mocker: MockFixture,
) -> unittest.Mock:
    """
    Create a random page from Wikipedia to use in future tests.

    :param mocker: A mocker object
    :type mocker: MockFixture
    :return: An object to mock the obtain_random_page() function from the
        wikipedia module
    :rtype: unittest.Mock
    """
    return mocker.patch("wiki_roulette.wikipedia.obtain_random_page")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: click.testing.CliRunner) -> None:
    """
    Test the main() function in a live environment.

    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(console.main)

    assert result.exit_code == 0


def test_main_succeeds(
    mock_requests_get: unittest.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Test whether the main() function of console.py succeeds.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    # An exit code of zero indicates the program was successful.
    assert result.exit_code == 0


def test_main_prints_title(
    mock_requests_get: unittest.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Test whether the main() function of console.py retrieves the article title.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    assert "Epictetus" in result.output


def test_main_invokes_requests_get(
    mock_requests_get: unittest.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Test whether the fixture actually invokes requests.get.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    runner.invoke(cli=console.main)

    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(
    mock_requests_get: unittest.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Test whether the CLI sends a request to the English Wikipedia.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    runner.invoke(cli=console.main)
    args = list(mock_requests_get.call_args.kwargs.values())

    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    mock_requests_get: unittest.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Test whether the CLI fails in an appropriate situations.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(cli=console.main)

    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    mock_requests_get: unittest.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Test whether main() outputs a message when we lack an Internet connection.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)

    assert "Error" in result.output


def test_main_uses_specified_language(
    mock_wikipedia_random_page: unittest.Mock,
    runner: click.testing.CliRunner,
) -> None:
    """
    Test whether main() outputs a message when we lack an Internet connection.

    :param mock_wikipedia_random_page: An object to mock the get() function
        from requests
    :type mock_wikipedia_random_page: unittest.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    language = "pl"
    runner.invoke(console.main, [f"--language={language}"])
    mock_wikipedia_random_page.assert_called_with(language=language)
