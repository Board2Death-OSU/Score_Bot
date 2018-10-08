import re
import discord
class Processor:

    def __init__(self):
        self.destination=""
    
    #Author:
    #   Jarod Klypchak
    #Description:
    #   Processes a discord message looking for the 2 letter country name and a positive or negative digit
    #Arguments:
    #   message: the message to be parsed
    #Return
    #   an array such that a[0]= {2 letter country code}
    #   and a[1]= a positive or negative digit
    def process_message(self,message):
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

        #Converts a UCT time to EST
    def process_time(self,msg):
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
    

    