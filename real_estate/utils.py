from twilio.rest import Client

def send_sms(to, body):
    account_sid = 'ACd62f36194b7defd0e91566231fc560b1'
    auth_token = 'b1b95dd71eda1634e7f4cfe7d600f2b3'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to,
        from_='+13156934355',
        body=body
    )

    return message.sid
