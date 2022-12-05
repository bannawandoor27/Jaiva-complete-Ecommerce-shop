# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from django.conf import settings
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC16200e195d4917cba56728779aebe4c8'
auth_token = 'd57a688fc7e550d63406ed2006a7610e'
client = Client(account_sid, auth_token)

service = client.messaging.v1.services.create(friendly_name='friendly_name')

print(service.sid)