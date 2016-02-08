import os, json
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Load config
with open('config.json') as json_data_file:
    config = json.load(json_data_file)

# Find these values at https://twilio.com/user/account
account_sid = os.getenv('TWILIO_ACCT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to=config['msg_to'], from_=config['msg_from'],
                                     body=config['msg_body'])
