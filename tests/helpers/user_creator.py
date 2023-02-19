from typing import List

from faker import Faker

from app.domains.users.repositories import UserModel
from tests.conftest import test_engine
from tests.helpers.model_factories import UserModelFactory
from tests.helpers.randoms import get_random_string

fake = Faker(locale="ko_KR")


def create_random_users(user_count: int = 10) -> List[UserModel]:
    users = []
    for _ in range(0, user_count):
        user_data = {
            "slack_id": get_random_string(20),
            "username": fake.name(),
            "avatar_url": fake.image_url(),
            "department": fake.company()
        }
        users.append(UserModelFactory(test_engine).build(**user_data))
    return users
