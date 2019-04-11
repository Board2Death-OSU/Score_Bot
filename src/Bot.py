from __future__ import print_function
import discord
from Spreadsheet import *
import asyncio
import re
from urllib.request import Request, urlopen
import json
import random
f=open("../data/data.json","r")
data=f.read()
f.close()
data=json.loads(data)
SPREADSHEET_ID=data["sheet_token"]
TOKEN2=data["discord_token"]
TOKEN="NTY1MjU2ODA2NTcwMzkzNjEx.XKzzBg.tJGs-9uBNzS335GJbNp_PW5ELzE"
countries=data["countries"]
counts=data["counts"]
responses=data["responses"]



do_useless_stuff=True
f=open("../data/dan_facts.txt","r")
dan_facts=f.read()
dan_facts=dan_facts.split("\n")
f.close()



"""
History:
    10/5/18: Created and Implemented - Jarod Klypchak
    1/31/19: Fixed to actually have the right time (maybe)-Jarod Klypchak
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
    4/9/19: Created and Implemented -Jarod Klypchak
Description:
    Gets a random fact about an animal.
Arguments:
    animal: the animal (dog,cat, or panda)
Return:
    The random fact, as a string.
"""
def get_fact(animal):
    req = Request('https://some-random-api.ml/facts/'+animal, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read().decode("utf-8")
    data=json.loads(page)
    return(data["fact"])

"""
History:
    4/9/19: Created and Implemented -Jarod Klypchak
Description:
    Gets a random picture of an animal.
Arguments:
    animal: the animal (dog,cat,panda,or pika)
Return:
    The relative/absolute path to the selected image.
"""
def get_pic(animal,total):
    num=random.randint(0,total)
    if animal=="pika":
        return "../data/img/"+animal+"/"+str(num)+".gif"
    else:
        return "../data/img/"+animal+"/"+str(num)+".jpg"

def get_dan_fact():
    num=random.randint(0,len(dan_facts))
    return(dan_facts[num])
class Bot:
    
    def __init__(self,countries,channel_name,token,spreadsheet):
        self.countries=countries
        self.bot=bot=discord.Client()
        self.channel_name=channel_name
        self.token=token
        self.spreadsheet=spreadsheet
        self.next_row=-1

    """
    History:
        4/9/19: Created and Implemented -Jarod Klypchak
    Description:
        Starts the discord bot.
    Arguments:
        None.
    Return:
        None.
    """
    def run(self):
        self.bot.run(self.token)

    """
    History:
        4/9/19: Created and Implemented -Jarod Klypchak
    Description:
        Processes a message being sent over discord, checking and executing the appropriate response.
    Arguments:
        message: the discord message.
    Return:
        A 3 tuple, with properties:
        channel: the channel the respond too.
        messages: all of the messages to send.
        option: 0 iff its a message, 1 if it's a file (img)
    """
    def handle_message(self,message):
        #Ensure The Message is not me =(
        if message.author==self.bot.user:
            return
        #Make sure it's the right channel
        elif str(message.channel)==self.channel_name:

            #Check If the Score needs to be sent.
            if message.content.upper().find("SCORE")>=0:
                temp=""
                temp=("Current PR Values for All Countries:\n")
                data=self.spreadsheet.read_column("CurrentPR/C","B","2","12")
                for i in range(len(data)):
                    temp=temp+(self.countries[i]+": "+data[i]+"\n")
                messages=[temp]
                return(message.channel,messagesk,0)

            #Check for PR Messages
            changes=self.process_message(message.content)
            if(changes!= None and len(changes)>1):
                changes.append(str(message.author.nick))
                messages=[]
                for i in range(len(changes[0])):
                    current=[process_time(message.id),changes[0][i],changes[1],message.author.nick]
                    if(self.next_row==-1):
                        self.next_row=self.spreadsheet.find_empty_cell_in_column("PRLog","D","2")
                    self.spreadsheet.write_row("PRLog","B","E",str(self.next_row),current)
                    msg=(current[1]+" gets "+current[2]+" PR "+str(message.author.nick)).format(message)
                    messages.append(msg)
                    self.next_row=self.next_row+1
                return(message.channel,messages,0)
        #No Comment
        if do_useless_stuff:
            if str(message.channel)=="off-topic":
                if "DAN FACT" in message.content.upper():
                    messages=[]
                    messages.append(get_dan_fact())
                    return (message.channel,messages,0)
                temp=re.search(r'(CAT FACT|DOG FACT|PANDA FACT|CAT PIC|DOG PIC|PANDA PIC|PIKA PIC)',message.content.upper())
                if temp!=None:
                    temp=temp.group(0)
                    messages=[]
                    value=0
                    animal=temp.split()[0].lower()
                    if "FACT" in temp:
                        messages.append(get_fact(animal))
                    elif "PIC" in temp:
                        messages.append(get_pic(animal,counts[animal]))
                        value=1
                    return (message.channel,messages,value)
                else:
                    messages=[]
                    for key in responses:
                        if key in message.content.upper():
                            messages.append(responses[key])
                    if len(messages)>0:
                        return(message.channel,messages,0)


    """
    History:
        10/5/18: Created and Implemented - Jarod Klypchak
        3/8/19: Updated to Proper 2019 country values -Jarod Klypchak
    Description:
        Processes a discord message, seeing if it represents a change in PR
    Arguments:
        message: a string that represents a message from discord
    Return:
        If message is of form [country code] [pr change]
        result[0]= Array of all countries to be affected.
        result[1]= Number to change by.
    """
    #Processes a message in the designated channel, looking for a two letter country key, and a number.
    def process_message(self,message):
        message=message.upper()
        result=[]
        countries=[]
        matches=re.findall(r'(BR|CH|EG|FR|GE|IN|JA|RU|SA|UK|US|ALL)',message)
        for match in matches:
            countries.append(str(match))
        if len(countries)>0:
            result.append(countries)
        match=re.search(r'\+?-? ?\d+',message)
        if(match != None):
            result.append(match.group())
        if(len(result) < 2):
            result=None
        return result

    """
    History:
        10/5/18: Created and Implemented -Jarod Klypchak
    Description:
        Prints a message, finds the current channel, and constructs a message to be sent.
    Arguments:
        None.
    Return:
        A tuple, with the channel and msg to be sent.
    """
    def handle_ready(self):
        print("Logged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("------------")

        msg="Jarod's WTS_Bot reporting for duty!"
        channels=self.bot.get_all_channels()
        for channel in channels:
            if str(channel)==self.channel_name:
                return (channel,msg)

spreadsheet=Spreadsheet(SPREADSHEET_ID)
wrapper=Bot(countries,"human",TOKEN,spreadsheet)

@wrapper.bot.event
async def on_message(message):
    result=wrapper.handle_message(message)
    if(result!=None):
        channel=result[0]
        messages=result[1]
        option=result[2]
        for message in messages:
            if option==0:
                await wrapper.bot.send_message(channel, message)
            elif option==1:
                await wrapper.bot.send_file(channel,message)

@wrapper.bot.event
async def on_ready():
    channel,msg=wrapper.handle_ready()
    #await wrapper.bot.send_message(channel,msg)

