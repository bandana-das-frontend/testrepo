import boto3
import requests
import http.client


def send_sns_sms(phone_number, message):
    # client = boto3.client(
    #     "sns",
    #     aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
    #     aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
    #     region_name="ap-southeast-1"
    # )
    #
    # status = client.publish(
    #     PhoneNumber="+91" + phone_number,
    #     Message=message,
    #     MessageAttributes={
    #             'AWS.SNS.SMS.SMSType': {
    #             'DataType': 'String',
    #             'StringValue': 'Promotional'
    #         }
    #     }
    # )

    url = "http://api.msg91.com/api/sendhttp.php?authkey=151272AF7gJ5pJKjR2590b38a0&mobiles={0}&message={1}&sender=COMMUN&route=4&country={2}".format(
        "91" + phone_number, message, "91")
    r = requests.get(url)


def send_promotional_sms(phone_number, message):
    url = "http://api.msg91.com/api/sendhttp.php?authkey=151272AF7gJ5pJKjR2590b38a0&mobiles={0}&message={1}&sender=COMMUN&route=1&country={2}".format(
        "91" + phone_number, message, "91")
    r = requests.get(url)


def send_msg91_sms(country_code, phone_number, message):

    url = "http://api.msg91.com/api/sendhttp.php"

    params = [('authkey', '151272AF7gJ5pJKjR2590b38a0'),
              ('mobiles', phone_number),
              ('message', message),
              ('sender', 'MILOAP'),
              ('route', 4),
              ('country', country_code)]

    r = requests.get(url, params=params)


def send_msg91_otp(phone_number, otp_code, extra_param):

    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = ""

    headers = {'content-type': "application/json"}
    url = "/api/v5/otp?invisible=1&otp="+otp_code+"&authkey=151272AF7gJ5pJKjR2590b38a0&mobile="+phone_number+"&template_id=5ddfa798d6fc053be626847a&extra_param=" + extra_param
    conn.request("POST", url, payload, headers)
    res = conn.getresponse()


def send_2factor_otp(phone, otp):
    requests.get("https://2factor.in" + "/API/V1/2b932bce-ff7a-11ea-9fa5-0200cd936042/SMS/" + phone + "/" + otp + "/Argus" )
