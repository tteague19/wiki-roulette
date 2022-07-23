"""Test the function in console.py."""
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
) -> unittest.mock.Mock:
    """
    Create a random page from Wikipedia to use in future tests.

    :param mocker: A mocker object
    :type mocker: MockFixture
    :return: An object to mock the obtain_random_page() function from the
        wikipedia module
    :rtype: unittest.mock.Mock
    """
    return mocker.patch("wiki_roulette.wikipedia.obtain_random_page")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: click.testing.CliRunner) -> None:
    """
    Return a status code of zero via the main() function in a live environment.

    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(console.main)

    assert result.exit_code == 0


def test_main_succeeds(
    mock_requests_get: unittest.mock.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Return a status code of zero via the main() function.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    # An exit code of zero indicates the program was successful.
    assert result.exit_code == 0


def test_main_prints_title(
    mock_requests_get: unittest.mock.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Retrieve the title of an article via the main() function.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    assert "Epictetus" in result.output


def test_main_invokes_requests_get(
    mock_requests_get: unittest.mock.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Invoke requests.get().

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    runner.invoke(cli=console.main)

    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(
    mock_requests_get: unittest.mock.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Send a request to the English Wikipedia via the CLI.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    runner.invoke(cli=console.main)
    args = list(mock_requests_get.call_args.kwargs.values())

    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    mock_requests_get: unittest.mock.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Cause a failure via the CLI.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(cli=console.main)

    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    mock_requests_get: unittest.mock.Mock, runner: click.testing.CliRunner
) -> None:
    """
    Provide an output message via main() when an Internet connection is absent.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)

    assert "Error" in result.output


def test_main_uses_specified_language(
    mock_wikipedia_random_page: unittest.mock.Mock,
    runner: click.testing.CliRunner,
) -> None:
    """
    Use a specified language with main().

    :param mock_wikipedia_random_page: An object to mock the get() function
        from requests
    :type mock_wikipedia_random_page: unittest.mock.Mock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    language = "pl"
    runner.invoke(console.main, [f"--language={language}"])
    mock_wikipedia_random_page.assert_called_with(language=language)
