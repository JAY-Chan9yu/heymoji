from unittest import mock

import pytest


@pytest.fixture(scope='function')
def mock_special_emoji():
    with mock.patch(
        'app.domains.reactions.services.settings.config.SPECIAL_EMOJI',
        "👍"
    ) as special_emoji:
        yield special_emoji
