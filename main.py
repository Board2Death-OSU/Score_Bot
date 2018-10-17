#!/usr/bin/python3
from __future__ import print_function
import discord
import asyncio
import threading
from helper import *
import time

"""
Useful Globals
"""

channel_name="general"
TOKEN="NDk3OTM2OTE5MDQxNDA5MDI4.DqE4bw.nmTQJThgPD4b0LzKx5bHosZ3YJQ"
client=discord.Client()
changes=[]
countries=["BR","CH","EG","FR","GE","IN","JA","RU","SA","UK","US"]

"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
Description:
    Handles when the discord client receives a message.
Arguments:
    message: the discord message
Return:
    None.
"""
@client.event
async def on_message(message):
    #Ensure The Message is not me =(
    if message.author==client.user:
        return

    #Make sure it's the right channel
    elif str(message.channel)==channel_name:
        a=process_message(message.content)
        a.append(str(message.author.nick))
        if(len(a)!=2):
            a.append(process_time(message.id))
            write(a)
            changes.append((a[0]+" gets "+a[1]+" PR from "+str(message.author.nick)))
            msg=(a[0]+" gets "+a[1]+" PR from "+str(message.author.nick)).format(message)
            await client.send_message(message.channel, msg)

def discord_thread():
    client.run(TOKEN);

"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
Description:
    Handles when the discord client logs in, notifying the relevant room.
Arguments:
    None.
Return:
    None.
"""
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

discord_thread=threading.Thread(target=discord_thread)
discord_thread.daemon=True
discord_thread.start()
time.sleep(5)
running=True
while(running):
    print("Options")
    print("[1]: Enter PR Change")
    print("[2]: Print Current PR Values")
    print("[3]: View Recent Changes")
    print("[4]: Exit")
    text=input("Please Enter Your Choice: ")
    choice=int(text)
    if(choice==1):
        manual_change(changes)
    elif(choice==2):
        scores=get_scores()
        for i in range(0,11):
            print(countries[i]+": "+scores[i])
    elif(choice==3):
        print_change_history(changes)
    elif(choice==4):
        running=False       
    else:
        print("Please Enter a Valid Option")

client.logout()

