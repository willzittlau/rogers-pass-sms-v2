from status import get_status, get_status_now
import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

# Send SMS
def send_update():
    from app import client
    from app import db
    from models import Info, User
    # Return contents for sms message
    todays_date = datetime.datetime.utcnow().date()
    daily_update_sms = db.session.query(Info.status).filter(Info.status_date == todays_date).limit(1).scalar()
    daily_update_sms = daily_update_sms.replace('\n', '\n\n')
    # Find list of numbers to send sms to
    daily_numbers = User.query.filter_by(status="yes").all()
    for number in daily_numbers:
        message = client.messages.create(
        from_=os.environ['TWILIO_NUMBER'],
        to=number.number,
        body=daily_update_sms
        )

def send_hello(number):
    from app import client
    message = client.messages.create(
        from_=os.environ['TWILIO_NUMBER'],
        to=number,
        body="Welcome to Roger's Pass SMS updates. To receive an update, reply with \"UPDATE\". Standard message rates apply."
    )

def confirm_in():
    body="You have successfully opted in for daily updates. To stop receiving updates, reply with \"NO\"."
    return body

def confirm_out():
    body="You have successfully opted out of daily updates. To opt back in, reply with \"YES\"."
    return body

def unknown_resp():
    body="Sorry, that was an unknown response. To receive an update, reply with \"UPDATE\"."
    return body

def update_now():
    body = get_status_now()
    return body