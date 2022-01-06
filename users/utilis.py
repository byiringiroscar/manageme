import requests


import os
from twilio.rest import Client

account_sid = "AC38cd1fd291baf345733f4a85cb167cea"
auth_token = "3c579f2c10c9575d99b992d8ac1ac844"
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Confirm this Pin in order to login - {user_code}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    print(r.json(), r.status_code)



