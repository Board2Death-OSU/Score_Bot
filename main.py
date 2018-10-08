#!/usr/bin/python3
from __future__ import print_function
import discord
import re
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from processor import Processor

channel_name="human"
TOKEN="NDk4MTU0ODg1NjI0MjMzOTk0.Dppmww._OVo7aW1IQv_KAn5IscnPg_wqOg"
SPREADSHEET_ID="1f720WIVi8aRfeUW78FkUexdjyuQbrNBK_0qhRpbxHbk"
client=discord.Client()
p=Processor()


#Writes a message to specified google sheets
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
    

exterminations=[]
#Handles receiving a message.
@client.event
async def on_message(message):
    #Ensure The Message is not me =(
    if message.author==client.user:
        return

    #Make sure it's the right channel
    elif str(message.channel)==channel_name:
        a=p.process_message(message.content)
        if(a!=None):
            a.append(str(message.author.nick))
            a.append(p.process_time(message.id))
            write(a)
            print((a[0]+" gets "+a[1]+" PR from "+str(message.author.nick)))#[:-5]))
            msg=(a[0]+" gets "+a[1]+" PR from "+str(message.author.nick)).format(message)
            await client.send_message(message.channel, msg)
    if("good bot" in message.content):
        msg="Good Human.".format(message)
        await client.send_message(message.channel, msg)
    elif("bad bot" in message.content):
        msg="You have been added to the list of pending exterminations.".format(message)
        
        exterminations.append(str(message.author.nick))
        msg=("You have been added to the list of pending exterminations.\n"+"Pending Exterminations: "+str(exterminations)).format(message)
        await client.send_message(message.channel, msg)

#Logs in the Bot
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------------")

    msg="Jarod's Human_Control_Bot reporting for duty!"
    channels=client.get_all_channels()
    for channel in channels:
        if str(channel)==channel_name:
            await client.send_message(channel,msg)

client.run(TOKEN)



