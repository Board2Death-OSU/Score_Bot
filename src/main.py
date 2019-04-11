#!/usr/bin/python3
from __future__ import print_function
import discord
import asyncio
import threading
import time

from Spreadsheet import *
from Bot import *



def manual_change():
    country=input("Please Enter the Country: ")
    number=input("Please Enter the PR Change: ")
    time=str(datetime.datetime.now())
    hours=time[11:13]
    minutes=time[14:16]
    hours=int(hours)
    hours-=12
    if hours<=0:
        hours+=12
    hours=str(hours)    
    time=hours+":"+minutes
    change=[time,country,number,"BOT OPERATOR"]
    if(wrapper.next_row==-1):
        wrapper.next_row=spreadsheet.find_empty_cell_in_column("PRLog","D","2")
    spreadsheet.write_row("PRLog","B","E",str(wrapper.next_row),change)
    wrapper.next_row=wrapper.next_row+1


#client=discord.Client()
def discord_thread():
    wrapper.run()

discord_thread=threading.Thread(target=discord_thread)
discord_thread.daemon=True
discord_thread.start()
time.sleep(5)
running=True
while(running):
    print("Options")
    print("[1]: Enter PR Change")
    print("[2]: Print Current PR Values")
    print("[3]: Exit")
    text=input("Please Enter Your Choice: ")
    choice=int(text)
    if(choice==1):
        manual_change()
    elif(choice==2):
        c_values=spreadsheet.read_column("CurrentPR/C","C","2","12")
        for i in range(len(countries)):
            print(countries[i]+": "+c_values[i])
    elif(choice==3):
        running=False       
    else:
        print("Please Enter a Valid Option")
wrapper.bot.logout()

