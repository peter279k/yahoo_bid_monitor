import os
import csv
import json
import requests


email_html = './index.html'
email_auth_path = './email_auth.txt'
email_setting = './mail_setting.csv'
email_addresses = './mail_addresses.csv'
if os.path.isfile(email_auth_path) is False:
    print('Cannot find the email_auth.txt file!')
    exit(1)

if os.path.isfile(email_html) is False:
    print('Do you generate the index.html email contents?')
    exit(1)

if os.path.isfile(email_setting) is False:
    print('Do you create the email_setting.csv file?')
    exit(1)

if os.path.isfile(email_addresses) is False:
    print('Do you create the email_addresses.csv file?')
    exit(1)

handler = open(email_html, 'r', encoding='utf-8')
email_contents = handler.read()
handler.close()

handler = open(email_auth_path, 'r')
api_key = handler.readlines()
handler.close()

if len(api_key) != 1:
    print('Do you set the email_auth.txt file correctly?')
    exit(1)


api_key = api_key[0].replace('\r', '')
api_key = api_key.replace('\n', '')


handler = open(email_setting, 'r')
email_setting = handler.readlines()
handler.close()

if email_setting[-1] == '':
    email_setting = email_setting[0:-1]
if len(email_setting) != 3:
    print('Do you set the mail_setting.csv file correctly?')
    exit(1)


subject = list(csv.reader([email_setting[0]]))[0][1]
sender_name = list(csv.reader([email_setting[1]]))[0][1]
sender_email = list(csv.reader([email_setting[2]]))[0][1]

handler = open(email_addresses, 'r')
email_addresses = handler.readlines()
handler.close()

if email_addresses[-1] == '':
    email_addresses = email_addresses[0:-1]

print('Sending bid data newsletter...')
api_url = 'https://api.sendinblue.com/v3/smtp/email'
headers = {
    'accept': 'application/json',
    'api-key': api_key,
    'content-type': 'application/json',
}
post_data = {
    'sender' : {
        'name': sender_name,
        'email': sender_email,
    },
    'to': [],
    'subject': subject,
    'htmlContent': email_contents,
}

for email_address in email_addresses:
    post_data['to'] = [{
        'email': email_address,
        'name': email_address.split('@')[0],
    }]
    post_data_json = json.dumps(post_data)
    response = requests.post(api_url, headers=headers, data=post_data_json)
    if response.ok is False:
        print(response.text)



print('Sending work is done.')
