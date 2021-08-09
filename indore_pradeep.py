import requests
import json
import sys
import time
import datetime
from datetime import timedelta
import logging
import pywhatkit
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "my_app.log"

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG) # better to have too much log than not enough
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   logger.propagate = False
   return logger

my_logger = get_logger("toto")
my_logger.debug("Outside of methods")


def get_request_params(current_date):

    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=314&date={current_date}"
    payload={}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    return url, payload, headers

def get_centers(current_date):

    url, payload, headers = get_request_params(current_date)
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        schedule_data = json.loads(response.text)
        return schedule_data['centers']
    except Exception as e:
        print(f"Error in get_centers - Error: {e}")

def check_vaccine_availability(centers):

    availability = {}
    if centers:
        for center in centers:
            if center['sessions']:
                for session in center['sessions']:
                    if int(session['min_age_limit']) == 18 and int(session['available_capacity_dose1']) > 0:
                        availability[center['pincode']] = f"{session['available_capacity_dose1']} {center['name']}"
    return availability

def get_vaccine_centers(session_data):

    vaccine_centers = []

    for location in session_data:
        address = location['address']
        vaccine_centers.append(address)

    return vaccine_centers

def get_message_time():
    now = datetime.datetime.now()
    message_time = now + timedelta(0, 60 - now.second)
    return message_time.hour, message_time.minute

def run():
    current_date = datetime.date.today().strftime("%d-%m-%Y")
    centers = get_centers(current_date)
    availability = check_vaccine_availability(centers)
    if availability:
        my_logger.debug(availability)
        message = f"Availability\n{availability}"
        hour, minute = get_message_time()
        # pywhatkit.sendwhatmsg('+917000323324', message, hour, minute)
    else:
        my_logger.debug('No availability')


while True:
    run()
    time.sleep(5)
