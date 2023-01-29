import random
import string


def get_random_string(length: int = 10) -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
