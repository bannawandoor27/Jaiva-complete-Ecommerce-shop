import os
from twilio.rest import Client


AUTH_TOKEN ='d57a688fc7e550d63406ed2006a7610e'
ACCOUNT_SID ='AC16200e195d4917cba56728779aebe4c8'

account_sid = ACCOUNT_SID
auth_token= AUTH_TOKEN
client = Client(account_sid, auth_token)
service = client.messaging.v1.services.create(friendly_name='banna')
print(service.sid)