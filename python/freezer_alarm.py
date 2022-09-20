#!/usr/bin/env python3

import pandas as pd
from gspread_pandas import Spread

### Import sheet
def import_sheet(sheet_id):
    sheet = Spread(sheet_id)
    df = sheet.sheet_to_df(index=None)
    df['temp_c'] = df['temp_c'].astype(float)
    return(df)

### Get the average temp over the last ten mins
def get_recent_average(input_df):
    tail = input_df.tail(5)
    average = tail['temp_c'].mean()
    return(average)

### Main
def main():
    # Importing the sheet and converting to data frame
    df = import_sheet("1KpIEUuMpRD8q3DDNNUeJ1BqSztl_nAzA8DWtdTHFnVY")
    print(df)

    # Getting the average temp over the last 10 mins (readings every 2 mins)
    recent_average = get_recent_average(df)
    print(recent_average)



if __name__ == "__main__":
    main()

