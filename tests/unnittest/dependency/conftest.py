from unittest import mock

import pytest

from tests.helpers.randoms import get_random_string


@pytest.fixture(scope='function')
def mock_challenge_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "challenge": get_random_string(20),
            "token": get_random_string(20),
            "type": "http"
        }
    ) as mock_request_body:
        yield mock_request_body


@pytest.fixture(scope='function')
def mock_bot_direct_message_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "event": {
                "bot_profile": {
                    "ts": "1609878469.036400",
                    "id": "ABCDEFG",
                    "deleted": False,
                    "name": "my-bot-name",
                    "updated": 1608584973,
                    "app_id": "<omitted>",
                    "icons": {
                        "image_36": "...",
                        "image_48": "...",
                        "image_72": "..."
                    },
                    "team_id": "abc1234"
                },
                "event_ts": "1609878469.036400",
                "type": "mention",
                "user": get_random_string(),
            },
            "bot_id": "ABCDEFG",
            "type": "message",
            "text": "Test message",
            "user": "12345678",
            "ts": "1609878469.036400",
            "team": "jay-team",
            "token": get_random_string(10),
            "team_id": get_random_string(10),
            "api_app_id": get_random_string(10),
            "event_id": get_random_string(10),
            "event_time": 1609878469,
            "is_ext_shared_channel": True,
            "event_context": get_random_string(10),
            "authorizations": []
        }
    ) as mock_bot_direct_message_body:
        yield mock_bot_direct_message_body


@pytest.fixture(scope='function')
def mock_slack_mention_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "event": {
                "type": "app_mention",
                "user": get_random_string(),
                "text": get_random_string(20),
                "channel": get_random_string(5),
                "event_ts": "1609878469.036400",
            },
            "bot_id": "ABCDEFG",
            "type": "message",
            "text": "Test message",
            "user": "12345678",
            "ts": "1609878469.036400",
            "team": "jay-team",
            "token": get_random_string(10),
            "team_id": get_random_string(10),
            "api_app_id": get_random_string(10),
            "event_id": get_random_string(10),
            "event_time": 1609878469,
            "is_ext_shared_channel": True,
            "event_context": get_random_string(10),
            "authorizations": []
        }
    ) as mock_slack_mention_body:
        yield mock_slack_mention_body


@pytest.fixture(scope='function')
def mock_slack_evnet_request():
    with mock.patch(
        'app.api.dependency.requests.Request.json',
        return_value={
            "event": {
                "type": "reaction_added",
                "user": get_random_string(),
                "item_user": get_random_string(),
                "text": get_random_string(20),
                "channel": get_random_string(5),
                "event_ts": "1609878469.036400",
                "reaction": "heart",
                "item": {},
            },
            "bot_id": "ABCDEFG",
            "type": "message",
            "text": "Test message",
            "user": "12345678",
            "ts": "1609878469.036400",
            "team": "jay-team",
            "token": get_random_string(10),
            "team_id": get_random_string(10),
            "api_app_id": get_random_string(10),
            "event_id": get_random_string(10),
            "event_time": 1609878469,
            "is_ext_shared_channel": True,
            "event_context": get_random_string(10),
            "authorizations": []
        }
    ) as mock_slack_mention_body:
        yield mock_slack_mention_body
