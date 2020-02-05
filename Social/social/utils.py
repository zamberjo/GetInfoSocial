
import os
import re


def save_file(file_path, values):
    values = [e for e in list(set(values)) if '\n' != e]
    with open(file_path, "w") as f:
        f.write("\n".join(values))


def check_user(user):
    return bool(user.id == os.environ["TELEGRAM_USER_ID"])


def check_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
