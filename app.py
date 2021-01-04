# Import libraries
import os
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from selenium import webdriver
import pandas as pd
import datetime
import time
import re
import platform
# import .py's
from sms import send_update, confirm_in, confirm_out, send_hello, unknown_resp, update_now
from status import get_status
from filters import is_valid_number, format_e164, numregex

# Set up app and environment
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['LOCAL_DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ['TZ'] = 'UTC'
if platform.system()!="Windows":
    time.tzset()

# Set up Twilio
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Create dB
db = SQLAlchemy(app)
from models import *

# Home Page
@app.route("/", methods =['GET', 'POST'])
def index():
    # Set dummy variable for Jinja and dB entry
    postsuccess = ''
    # POST request route
    if request.method == 'POST':
        # Get data from form and fill dB variables
        number_in = request.form.get('number')
        signup_date = datetime.datetime.utcnow().date()
        posttime = datetime.datetime.utcnow()
        # Verify number and prevent incorrect form entries
        number_out = numregex(number_in)
        # Format to e.164 for dB entry
        number = format_e164(number_out)
        if is_valid_number(number) and number != '':
            # Check if user has already signed up for the udpate or not
            if bool(User.query.filter_by(number=number).first()) == False:
            # Append to dB
                status = "no"
                data = User(number, status, signup_date)
                db.session.add(data)
                db.session.commit()
                # Send Message and update Jinja variable
                send_hello(number)
                postsuccess = 'posted'
        # Redirects with error flash
            else:
                flash('This number has already been signed up for SMS updates!', 'error')
                return redirect(url_for('index'))
        else:
            flash('Error: Phone number doesn\'t exist or incorrect format. Please try again!', 'error')
            return redirect(url_for('index'))
    # Return template
    return render_template('index.html', postsuccess=postsuccess)

@app.route("/twilio", methods=['POST'])
def sms_reply():
    message_body = request.form['Body'].lower()
    number = request.form['From']
    message_date = datetime.datetime.utcnow().date()
    if message_body == "yes":
        # Check if name entry exists
        if bool(User.query.filter_by(number=number).first()) == True:
            # Modify selected area
            user = User.query.filter_by(number=number).first()
            user.status = message_body
            # Submit changes to dB
            db.session.commit()
        # Add entry to dB if it doesn't already exist
        else:
            data = User(number, message_body, message_date)
            db.session.add(data)
            db.session.commit()
        # Send opt in message
        resp = MessagingResponse()
        resp.message(confirm_in())
        return str(resp)
    if message_body == "no":
        # Check if name entry exists
        if bool(User.query.filter_by(number=number).first()) == True:
            # Modify selected area
            user = User.query.filter_by(number=number).first()
            user.status = message_body
            # Submit changes to dB
            db.session.commit()
        # Add entry to dB if it doesn't already exist
        else:
            data = User(number, message_body, message_date)
            db.session.add(data)
            db.session.commit()
        resp = MessagingResponse()
        resp.message(confirm_out())
        return str(resp)
    if message_body == "update":
        # Check if name entry exists
        if bool(User.query.filter_by(number=number).first()) == True:
            pass
        else:
            data = User(number, "no", message_date)
            db.session.add(data)
            db.session.commit()
        resp = MessagingResponse()
        resp.message(update_now())
        return str(resp)
    else:
        # Check if name entry exists
        if bool(User.query.filter_by(number=number).first()) == True:
            pass
        else:
            data = User(number, "no", message_date)
            db.session.add(data)
            db.session.commit()
        resp = MessagingResponse()
        resp.message(unknown_resp())
        return str(resp)

# On running app.py, run Flask app
if __name__ == "__main__":
    # Still under development, run debug
    app.run(debug=True)
