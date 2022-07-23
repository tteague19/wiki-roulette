"""Test functions in the wikipedia.py module."""
from unittest.mock import Mock

import click
import pytest

from wiki_roulette import wikipedia
from wiki_roulette.wikipedia import WikipediaPage


def test_obtain_random_page_uses_given_language(
    mock_requests_get: Mock,
) -> None:
    """
    Use the language specification capability of obtain_random_page().

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: Mock
    """
    wikipedia.obtain_random_page(language="de")
    args = list(mock_requests_get.call_args.kwargs.values())

    assert "de.wikipedia.org" in args[0]


def test_obtain_random_page_returns_wikipedia_page_object(
    mock_requests_get: Mock,
) -> None:
    """
    Return a WikipediaPage object via the obtain_random_page() function.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: Mock
    """
    page = wikipedia.obtain_random_page(language="en")
    assert isinstance(page, WikipediaPage)


def test_obtain_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    """
    Raise an error when the obtain_random_page() receives invalid data.

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: Mock
    """
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.obtain_random_page(language="en")
