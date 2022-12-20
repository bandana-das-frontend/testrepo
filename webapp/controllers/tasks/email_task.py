from django.core.mail import send_mail
from webapp.dbplatform import *
from datetime import datetime
import pytz


def send_mail_to_tech(subject, message=""):
    # 'Asia/Colombo'
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.now(pytz.timezone('UTC'))
    now_india = now_utc.astimezone(pytz.timezone('Asia/Colombo'))

    if settings.DEBUG is True:
        send_mail(subject, "[Dev]: " + message + '\n' + str(now_india), 'chipmunk@glynk.com', ['rajkumar@glynk.com', 'laxman@glynk.com'], fail_silently=True)
    else:
        send_mail(subject, message + '\n' + str(now_india), 'chipmunk@glynk.com', ['tech-notif@glynk.com'], fail_silently=True)
