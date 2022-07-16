from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_requests_get(
    mocker: MockerFixture,
) -> Mock:
    """
    Create a mock object to mock a GET request.

    :param mocker: A mocker object
    :type mocker: MockerFixture
    :return: An object to mock the get() function from requests
    :rtype: Mock
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
