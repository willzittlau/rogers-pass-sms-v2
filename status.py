# Import libraries
import os
from selenium import webdriver
import pandas as pd
import datetime
import time
import re

# Webscrape data and add to dB
def get_status():
    from app import db
    from models import Info
    # Selenium init
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ['GOOGLE_CHROME_PATH']
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], chrome_options=chrome_options)
    # Scrape
    driver.get('https://www.pc.gc.ca/apps/rogers-pass/print?lang=en')
    time.sleep(5)
    page_source = driver.page_source
    statusDate = driver.find_element_by_id('publishDate').text
    driver.quit()
    # Save data
    tables = pd.read_html(page_source)
    wra_table = pd.DataFrame(tables[0])
    parking_table = pd.DataFrame(tables[1])
    prohibited_table = pd.DataFrame(tables[2])
    # Initialise strings
    title_string = statusDate + ':'
    wra_open_string = 'Open WRAs: '
    wra_closed_string = 'Closed WRAs: '
    parking_open_string = 'Open Parking: '
    parking_closed_string = 'Closed Parking: '
    prohibited_string = 'Prohibited Areas: '
    # String concatenation for WRA table
    for i in range (0, len(wra_table['Winter Restricted Area'])):
        if wra_table.at[i, 'Status'].startswith('O'):
            wra_table.at[i, 'Status'] = wra_table.at[i, 'Status'][:4]
            wra_open_string += (wra_table.at[i, 'Winter Restricted Area'] + ', ')
        if wra_table.at[i, 'Status'].startswith('C'):
            wra_table.at[i, 'Status'] = wra_table.at[i, 'Status'][:6]
            wra_closed_string += wra_table.at[i, 'Status'] + '\n'
    if not wra_open_string.endswith(': '):
        wra_open_string = wra_open_string[:-2]
    if not wra_closed_string.endswith(': '):
        wra_closed_string = wra_closed_string[:-2]
    # String concatenation for Parking table
    for i in range (0, len(parking_table['Parking area'])):
        parking_table.at[i,'Parking area'] = parking_table.at[i,'Parking area'].replace(' Parking', '')
        if parking_table.at[i, 'Status'].startswith('O'):
            parking_table.at[i, 'Status'] = parking_table.at[i, 'Status'][:4]
            parking_open_string += (parking_table.at[i, 'Parking area'] + ', ')
        if parking_table.at[i, 'Status'].startswith('C'):
            parking_table.at[i, 'Status'] = parking_table.at[i, 'Status'][:6]
            parking_closed_string += parking_table.at[i, 'Status'] + '\n'
    if not parking_open_string.endswith(': '):
        parking_open_string = parking_open_string[:-2]
    if not parking_closed_string.endswith(': '):
        parking_closed_string = parking_closed_string[:-2]
    # String concatenation for Prohibited table
    for i in range (0, len(prohibited_table['Winter Prohibited Area'])):
        prohibited_string += (prohibited_table.at[i, 'Winter Prohibited Area'] + ', ')
    if not prohibited_string.endswith(': '):
        prohibited_string = prohibited_string[:-2]
    # Concat and save results for dB
    status = (title_string + '\n' + wra_open_string 
                + '\n' + wra_closed_string + '\n' + parking_open_string 
                + '\n' + parking_closed_string + '\n' + prohibited_string)
    status_date = datetime.datetime.utcnow().date()
    # Append to dB
    rpdata = Info(status, status_date)
    db.session.add(rpdata)
    db.session.commit()