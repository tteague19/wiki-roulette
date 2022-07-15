import unittest

import pytest
import pytest_mock


@pytest.fixture()
def mock_requests_get(
    mocker: pytest_mock.plugin.MockerFixture,
) -> unittest.mock.MagicMock:
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
                "his pupil Arrian in his Discourses and Enchiridion.",
            ]
        ),
    }

    return mock


def pytest_configure(config: pytest.Config) -> None:
    """
    Register the e2e hook.

    :param config: An object to configure PyTest
    :type config: pytest.Config
    """
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
