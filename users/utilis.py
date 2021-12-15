import os
from twilio.rest import Client

account_sid = "ACe991a8e88df38d4f42d09211d69d4d70"
auth_token = "4e490f54b9c09376dddfd84755118b3e"
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages \
        .create(
        body=f"hi your verification code from ManageMe is - {user_code}",
        from_='+12564880494',
        to=f'{phone_number}'
    )

    print(message.sid)

