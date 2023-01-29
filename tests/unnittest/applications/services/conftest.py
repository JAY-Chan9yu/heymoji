from app.applications.schemas import SlackEvent
from app.domains.reactions.entities import SlackEventType
from tests.helpers.randoms import get_random_string


def get_mock_slack_evnet(user_slack_id: str, item_user_slack_id: str, reaction: str):
    return SlackEvent(
        type=SlackEventType.ADDED_REACTION.value,
        user=user_slack_id,
        item_user=item_user_slack_id,
        reaction=reaction,
        text=get_random_string(),
        channel=get_random_string(),
        event_ts="1609878469.036400",
        item={}
    )
