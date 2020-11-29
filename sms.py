from status import get_status
import os

# Send SMS
def send_update(number):
    from app import client
    # Return contents for sms message
    todays_date = datetime.datetime.utcnow().date()
    # daily_update_sms = db.session.query(Info.status).filter(Info.status_date == todays_date).limit(1).scalar()
    # daily_update_sms = daily_update_sms.replace('\n', '\n\n')
    daily_update_sms = get_status()
    # # Find list of numbers to send sms to
    # daily_numbers = db.session.query(User.number.distinct()).filter(and_(User.status="yes")).all()
    # daily_numbers = [r for r, in daily_numbers]
    # for number in daily_numbers:
    #     message = client.messages.create(
    #         from_=os.environ['TWILIO_NUMBER'],
    #         to=number,
    #         body=daily_update_sms
    #     )
    message = client.messages.create(
        from_=os.environ['TWILIO_NUMBER'],
        to=number,
        body=daily_update_sms
    )

def send_hello(number):
    from app import client
    message = client.messages.create(
        from_=os.environ['TWILIO_NUMBER'],
        to=number,
        body="Thank you for signing up for the Roger's Pass SMS update service. To start receiving daily updates, reply with \"YES\". Standard message rates apply."
    )

def confirm_in():
    body="You have successfully opted in for daily updates. To stop receiving updates, reply with \"NO\"."
    return body

def confirm_out():
    body="You have successfully opted out of daily updates. To opt back in, reply with \"YES\"."
    return body

def unknown_resp():
    body="Sorry, that was an unknown response. To start receiving daily updates, reply with \"YES\". To stop receiving updates, reply with \"NO\"."
    return body