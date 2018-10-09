#!/usr/bin/python3
from __future__ import print_function
import discord
import threading
from helper import *
import time

"""
Useful Globals
"""

channel_name="coding-do-not-disturb"
TOKEN="NDk3OTM2OTE5MDQxNDA5MDI4.Dp5Vdg.yiUYqoxAWXsTfg3pcu3_-3HlNa8"
client=discord.Client()

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
            print((a[0]+" gets "+a[1]+" PR from "+str(message.author.nick)))#[:-5]))
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

#client.run(TOKEN)

threading.Thread(target=discord_thread).start()