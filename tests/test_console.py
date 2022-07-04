import unittest.mock

import click.testing
import pytest
import pytest_mock

from wiki_roulette import console


@pytest.fixture()
def mock_requests_get(
        mocker: pytest_mock.plugin.MockerFixture) -> unittest.mock.MagicMock:
    """
    Create a mock object to mock a GET request.

    :param mocker: A mocker object
    :type mocker: pytest_mock.plugin.MockerFixture
    :return: An object to mock the get() function from requests
    :rtype: unittest.mock.MagicMock
    """
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Epictetus",
        "extract": " ".join(
            [
                "Epictetus was a Greek Stoic philosopher.",
                "He was born into slavery at Hierapolis, Phrygia and",
                "lived in Rome until his banishment, when he went to",
                "Nicopolis in northwestern Greece for the rest of his",
                "life. His teachings were written down and published by",
                "his pupil Arrian in his Discourses and Enchiridion."
            ]
        )
    }

    return mock


@pytest.fixture()
def runner() -> click.testing.CliRunner:
    """Create an object to invoke the CLI."""
    return click.testing.CliRunner()


def test_main_succeeds(
        mock_requests_get: unittest.mock.MagicMock,
        runner: click.testing.CliRunner) -> None:
    """
    Test whether the main() function of console.py succeeds.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.MagicMock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    # An exit code of zero indicates the program was successful.
    assert result.exit_code == 0


def test_main_prints_title(
        mock_requests_get: unittest.mock.MagicMock,
        runner: click.testing.CliRunner) -> None:
    """
    Test whether the main() function of console.py retrieves the article title.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.MagicMock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    result = runner.invoke(cli=console.main)

    assert "Epictetus" in result.output


def test_main_invokes_requests_get(
        mock_requests_get: unittest.mock.MagicMock,
        runner: click.testing.CliRunner) -> None:
    """
    Test whether the fixture actually invokes requests.get.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.MagicMock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    runner.invoke(cli=console.main)

    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(
        mock_requests_get: unittest.mock.MagicMock,
        runner: click.testing.CliRunner) -> None:
    """
    Test whether the CLI sends a request to the English Wikipedia.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.MagicMock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    runner.invoke(cli=console.main)
    args = list(mock_requests_get.call_args.kwargs.values())

    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
        mock_requests_get: unittest.mock.MagicMock,
        runner: click.testing.CliRunner) -> None:
    """
    Test whether the CLI fails in an appropriate situations.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.MagicMock
    :param runner: An object to invoke the CLI
    :type runner: click.testing.CliRunner
    """
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(cli=console.main)

    assert result.exit_code == 1
