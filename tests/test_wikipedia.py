import unittest

from wiki_roulette import wikipedia


def test_obtain_random_page_uses_given_language(
        mock_requests_get: unittest.mock.MagicMock,
) -> None:
    """
    Test the language specification capability of obtain_random_page().

    :param mock_requests_get: An object to mock the get() function from
        requests
    :type mock_requests_get: unittest.mock.MagicMock
    """
    wikipedia.obtain_random_page(language="de")
    args = list(mock_requests_get.call_args.kwargs.values())

    assert "de.wikipedia.org" in args[0]
