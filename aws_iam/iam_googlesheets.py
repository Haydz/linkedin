'''
This script is designed to demonstrate a potetial use case for google sheets and the AWS SDK
It is meant to be run daily, it writes the AWS users it finds into google sheets in the column
of each day. It also prints to the screen if new users are found.

It works by identifying todays date, then pulling the first row of all columns of a googlespreadsheet,
finding the column for yesterdays dates. Pulls yesterdays columns data, then connects to the
AWS SDK to pull a list of all users (which becomes todays list). It compares yesterdays users
with todays list, to idetify any new users. It then writes todays users to googlespreadsheet.


Cloudtrail already alerts when new users are created, but this was an easy way to demonstrate
both services.


Expansion ideas:
- and more error handling
- sending an alert via slack of new users

'''

from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import boto3

import datetime

# If modifying these scopes, delete the file token.json.

def main():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    speadsheet_ID = 'xxxxxxxxxxxxxxxxxxxxxxx'
    #on windows you may need to use the full path for the credentails.json location
    credentials_location = "credentials.json"
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # If modifying these scopes, delete the file token.json.
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_location, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    #getting todays and the day befores date
    today = datetime.date.today()
    print("RUNNIN SCRIPT ON: {}".format(today))
    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    print("Yesterday's date:", yesterday_str)
    #for testing different dates
    # yesterday_str = "2023-05-27"

    #function for finding the new users
    def find_missing_words(array1, array2):
        missing_words = [word for word in array1 if word not in array2]
        return missing_words

    #function for calling the googlespreadsheest API to read data.
    def sheets(range_name):
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=speadsheet_ID,
                    range=range_name).execute()
        return result.get('values', [])


# == READING SHEET == 
    previous_users = []
    try:
        today_column_index = []
        yesterday_columns_index = []

        service = build('sheets', 'v4', credentials=creds)
        range_name = f'Sheet1!A1:ZZ1'  # NEED TO MAKE LONGER, - TILL END OF COLUMNS

        get_column_indexes = sheets(range_name)
        values = get_column_indexes
        if not values:
            print('No data found.')
            return
        if values:
            header_row = values[0]  # Assuming the first row contains the headers
            for col_index, header in enumerate(header_row):
                if header == yesterday_str:
                    today_column_index.append(col_index + 1)  # Add 1 to adjust for 0-based index
                else:
                    continue
    except HttpError as err:
        print(err)
    #collect values from yeterdays columns
    try:
            if today_column_index is not None:
                yesterday_columns_index = today_column_index[0] -1  # we -1 because chr 65 is A.
                #we then add the index the char of A
                #start from 2 so that we do not collect the header row
                range_name = f'Sheet1!{chr(65+yesterday_columns_index)}2:{chr(65+yesterday_columns_index)}100'
                get_yesterday_values = sheets(range_name)
            #collecting the values
            column_data = get_yesterday_values
            # Flatten the list and convert the values to strings
            flattened_list = [str(value) for sublist in column_data for value in sublist]
            previous_users = flattened_list
    except HttpError as err:
            print(err)


# == Write list of users into sheet -This is next, once read FIND NEW USERS
    try:
        #collect list from todays users
        iam = boto3.client('iam')
        users = iam.list_users()
       
        collected_users = []
        for user in users['Users']:
            # print(user['UserName'])
            collected_users.append(user['UserName'])
        
        #find missing users - different between arrays
        missing_users = find_missing_words(collected_users, previous_users)
        if missing_users:
            print("FOUND NEW USERS")
            print(missing_users)
        #creating list of previous users and adding new users to the end
        correct_order_users = previous_users + missing_users
        #adding date to array
        correct_order_users.insert(0, str(today))

        print('Building body to update google sheets')
        #creating sheets values in correct format
        values = [[value] for value in correct_order_users]
        # !print(values)
        body = {
            'values': values
        }
        write_column_name = chr(65 + today_column_index[0])
        # print("calculation of next column: ", write_column_name )
        #need to place in correct format to sent
        write_range_name = f'Sheet1!{write_column_name}1:{write_column_name}{len(correct_order_users)}'
        #no function because update only used once
        result = service.spreadsheets().values().update(
            spreadsheetId=speadsheet_ID, range=write_range_name,
            valueInputOption='RAW', body=body).execute()
    except HttpError as err:
        print(err)



#=== FIND PICKLE TOKEN ==
# import os
# def find_token_pickle():
#     for root, dirs, files in os.walk('.'):
#         if 'token.pickle' in files:
#             return os.path.abspath(os.path.join(root, 'token.pickle'))
    
#     return None

# # Usage
# token_pickle_path = find_token_pickle()
# if token_pickle_path:
#     print(f"Found token.pickle file at: {token_pickle_path}")
# else:
#     print("token.pickle file not found.")


if __name__ == '__main__':
    main()


    