import re
from twilio.base.exceptions import TwilioRestException

# Twilio number verification
def is_valid_number(number):
    from app import client
    try:
        response = client.lookups.phone_numbers(number).fetch(type="carrier")
        return True
    except TwilioRestException as e:
        if e.code == 20404:
            return False

# Convert input to e.164 format
def format_e164(number):
    number = number.replace('(','')
    number = number.replace(')','')
    number = number.replace('-','')
    number = number.replace('+','')
    number = number.replace('[','')
    number = number.replace(']','')
    number = number.replace('.','')
    number = number.replace(' ','')
    number = number.replace('·','')
    if len(number) > 10:
        if number.startswith('1'):
            number = '+' + number
        else:
            number = '+1' + number
    if len(number) == 10:
        number = '+1' + number
    return (number)

# Regex to sort only numbers
def numregex(number_in):
    num_regex = re.findall(r'''[^a-zA-Z@$&%!=:;/|}{#^*_\\><,?"']''', number_in)
    number_out = ''.join(num_regex)
    return number_out