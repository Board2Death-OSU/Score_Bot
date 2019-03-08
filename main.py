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

channel_name="INSERT HERE"
TOKEN="INSERT HERE"
client=discord.Client()
changes=[]
countries=["BRI","CAI","CAU","DRA","JAB","NID","NOB","SAL","SOL"]
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
        
        
        if(a!= None and len(a)>1):
            a.append(str(message.author.nick))
            for i in range(len(a[0])):
                current=[]
                current.append(a[0][i])
                current.append(a[1])
                current.append(message.author.nick)
                current.append(process_time(message.id))
                write(current)
                changes.append((current[0]+" gets "+current[1]+" PR from "+str(message.author.nick)))
                msg=(current[0]+" gets "+current[1]+" PR "+str(message.author.nick)).format(message)
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

    msg="Jarod's WTS_Bot reporting for duty!"
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
        for i in range(len(countries)):
            print(countries[i]+": "+scores[i])
    elif(choice==3):
        print_change_history(changes)
    elif(choice==4):
        running=False       
    else:
        print("Please Enter a Valid Option")

client.logout()

