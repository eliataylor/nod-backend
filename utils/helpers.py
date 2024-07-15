from twilio.rest import Client

from nod_base import settings

def send_sms(to, body):
    client = Client(settings.TWILIO_AUTH_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
    return message.sid
