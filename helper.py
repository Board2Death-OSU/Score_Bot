import discord
import re
from googleapiclient.discovery import build
import datetime
from httplib2 import Http
from oauth2client import file, client, tools
SPREADSHEET_ID=#Insert Spreadsheet ID

#A collection of helper methods for WTS_PR_BOT


"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
Description:
    Processes a discord message, seeing if it represents a change in PR
Arguments:
    message: a string that represents a message from discord
Return:
    If message is of form [country code] [pr change], result[0]=country code and result[1]= PR change
    Otherwise, result=None.
"""
#Processes a message in the designated channel, looking for a two letter country key, and a number.
def process_message(message):
        a=[]
        match=re.search(r'(BR|CH|EG|FR|GE|IN|JA|RU|SA|UK|US|ALL|Br|Ch|Fr|Ge|In|Ja|Ru|Eg|Sa|Uk|Us|All|br|ch|fr|eg|ge|in|ja|ru|sa|uk|us|all)',message)
        if(match != None):
            a.append(match.group())
        match=re.search(r'\+?-?\d+',message)
        if(match != None):
            a.append(match.group())
        if(len(a) < 2):
            a=None
        return a


"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
Description:
    Converts a discord_snowflake to an EST time in military time.
Arguments:
    msg: a discord snowflake
Return:
    a string that represents the time a message was sent in EST.
"""
def process_time(msg):
        time=str(discord.utils.snowflake_time(msg))
        time=time[11:-10]
        hours=time[:2]
        minutes=time[2:]
        hours=int(hours)
        hours-=4
        if hours<=0:
            hours+=12
        hours=str(hours)    
        return hours+minutes

"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
Description:
    Writes a message to specified google sheets
Arguments:
    message: an array of length 4 where
        message[0]=country code
        message[1]=PR change
        message[2]=Author of Change
        message[3]=Time
Return:
    None.
"""

def write(message):
    #Log in info
    global SPREADSHEET_ID
    SCOPES='https://www.googleapis.com/auth/spreadsheets'

    #Log into Google
    store=file.Storage('token.json')
    creds=store.get()
    if not creds or creds.invalid:
        flow=client.flow_from_clientsecrets('credentials.json',SCOPES)
        creds=tools.run_flow(flow,store)
    service=build('sheets','v4',http=creds.authorize(Http()))
    
    #Find first empty row
    RANGE_2 ="PRLog!C3:C"
    result=service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_2).execute()
    current_row=0
    result=result.get('values',[])
    current_row+=3+len(result)

    #Write Values to Spot
    RANGE_NAME ="PRLog!B"+str(current_row)+":E"+str(current_row)
    values=[
        [
            message[3],message[0], message[1],message[2]
        ]
    ]
    body={'values':values}
    result=service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME,valueInputOption="USER_ENTERED", body=body).execute()

def get_scores():
    #Log in info
    global SPREADSHEET_ID
    SCOPES='https://www.googleapis.com/auth/spreadsheets'

    #Log into Google
    store=file.Storage('token.json')
    creds=store.get()
    if not creds or creds.invalid:
        flow=client.flow_from_clientsecrets('credentials.json',SCOPES)
        creds=tools.run_flow(flow,store)
    service=build('sheets','v4',http=creds.authorize(Http()))

    
    RANGE_2 ="CurrentPR/RP!B3:B13"
    result=service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_2).execute()
    result=result.get('values',[])
    scores=[]
    for value in result:
        scores.append(value[0])
    return scores
"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
Description:
    Writes a message to specified google sheets
Arguments:
    message: an array of length 4 where
        message[0]=country code
        message[1]=PR change
        message[2]=Author of Change
        message[3]=Time
Return:
    None.
"""

def print_change_history(changes):
    print("Changes during this exectution:")
    for message in changes:
        print(message)
    print("----------------------------------")

def manual_change(changes):
    text=input("Please Enter Your PR Message: ")
    a=process_message(text)
    
    if(len(a)==2):
        changes.append((a[0]+" gets "+a[1]+" PR from BOT OPERATOR"))
        a.append("BOT OPERATOR")
        time=str(datetime.datetime.now())
        time=time[11:16]
        a.append(time)
        write(a)