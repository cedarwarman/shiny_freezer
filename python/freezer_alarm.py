#!/usr/bin/env python3

import os
import time
import pandas as pd
from gspread_pandas import Spread
import yagmail

### Import sheet
def import_sheet(sheet_id):
    sheet = Spread(sheet_id)
    df = sheet.sheet_to_df(index=None)
    df['temp_c'] = df['temp_c'].astype(float)
    return(df)

### Open log file
def open_log_file():
    log_file_path = os.path.join(os.getcwd(), "python_data", "freezer_alarm_log.tsv")
    if not os.path.exists(os.path.join(os.getcwd(), "python_data")):
        os.makedirs(os.path.join(os.getcwd(), "python_data"))

    try:
        f = open(log_file_path, 'a+')
        if os.stat(log_file_path).st_size == 0:
                f.write('date_time\tmessage\n')
        return(f)
    except:
        pass

### Append log file
def append_log_file(input_file_handle):
    try:
        input_file_handle.write(
            '{0}\t{1}\n'.format(
                time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(time.time())),
                'sent_alarm_email'
            )
        )
    except:
        print("Failed to update log file")

### Get the average temp over the last ten mins
def get_recent_average(input_df):
    tail = input_df.tail(5)
    average = tail['temp_c'].mean()
    return(average)

### Get time of last alarm email
def last_alarm():
    log_file = open_log_file()
    lines = log_file.readlines()
    print(lines)
    if len(lines) > 1:
        

### Send alarm email
def send_email():
    # Requires you to have initialized your username and password in yagmail:
    # yagmail.register('palanivelu.lab.freezer@gmail.com', 'password_here')
    # This stores your credentials in the local systen with Python keyring.
    yag = yagmail.SMTP('palanivelu.lab.freezer')
    contents = [
        "Alert! The freezer has warmed a dangerous amount. See details here:",
        "https://viz.datascience.arizona.edu/freezer/"
    ]
    yag.send('cedardalewarman@gmail.com', 'FREEZER ALARM', contents)

    # Append to log file that you've sent an email
    log_file = open_log_file()
    append_log_file(log_file)
    log_file.close()

### Main
def main():
    # Importing the sheet and converting to data frame
    df = import_sheet("1KpIEUuMpRD8q3DDNNUeJ1BqSztl_nAzA8DWtdTHFnVY")
    print(df)

    # Getting the average temp over the last 10 mins (readings every 2 mins)
    recent_average = get_recent_average(df)
    print(recent_average)

    # If the temp is greater than -65 then it will send an email. 
    # Calculating time since last alert sent
    
    # Sending email:
    send_email()



if __name__ == "__main__":
    main()

