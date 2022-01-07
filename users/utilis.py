import requests


def send_sms(user_code, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'Confirm this Pin in order to login - {user_code}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    # print(r.json(), r.status_code)


def send_sms_request(phone_number_lessor, phone_number_tenant, name, property_name):
    data = {
        'recipients': phone_number_lessor,
        'message': f'Tenant - {name} requested to use your Property: {property_name} and his Phone_number is {phone_number_tenant} you received this message because you are in ManageMe system',
        'sender': '+250786405263',
    }
    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    print(r.json(), r.status_code)


# send message to tenant that approved to use property
def send_sms_approve(phone_number_lessor, phone_number_tenant, name, property_name):
    data = {
        'recipients': phone_number_tenant,
        'message': f'Lessor - {name} Approved you to use This Property: {property_name} and his Phone_number is {phone_number_lessor} you received this message because you are in ManageMe system',
        'sender': '+250786405263',
    }
    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    print(r.json(), r.status_code)


# send message to tenant that denied to use this product
def send_sms_denied(phone_number_lessor, phone_number_tenant, name, property_name):
    data = {
        'recipients': phone_number_tenant,
        'message': f'Lessor - {name} Denied you to use This Property: {property_name} and his Phone_number is {phone_number_lessor} you received this message because you are in ManageMe system',
        'sender': '+250786405263',
    }
    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('byiringoroscar@gmail.com', 'oscarlewis.O1'))
    print(r.json(), r.status_code)
