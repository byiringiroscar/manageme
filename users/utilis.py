import os
from twilio.rest import Client

account_sid = "AC38cd1fd291baf345733f4a85cb167cea"
auth_token = "3c579f2c10c9575d99b992d8ac1ac844"
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages \
        .create(
        body=f"hi your verification code from ManageMe is - {user_code}",
        from_='+18164954060',
        to=f'{phone_number}'
    )

    print(message.sid)

