import random
import string


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
