from datetime import date


def get_age(user):
    if not user:
        return 0

    born = user.birthday
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
