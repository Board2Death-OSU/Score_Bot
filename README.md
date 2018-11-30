# WTS_PR_Bot
A bot that utilizes the Discord and Google Sheets API to automatically track changes to PR in Watch the Skies. First developed at OSU Board2Death's Watch the Skies AU2018

# HOW_TO_USE
    1.) Construct create a new Application through discord to generate your bot token. 
            https://discordapp.com/developers/applications
    2.) Insert the bot's specific token under TOKEN in main.py
    3.) Create a spreadsheet for the specific game in Google Sheets by copying from templates/spreadsheet.xlsx
    4.) Add the spreadsheet ID to SPREADSHEETID in main.py 
        A spreadsheet ID can be found in the URL of the spreadsheet. In the example below, the ID appears after /d/, with an ID of          abc1234567
            https://docs.google.com/spreadsheets/d/abc1234567/edit#gid=0
    6.) Add the bot to your Discord channel using the Discord OAUTH2 URL GENERATOR (from the link in step 1)
    
    7.) Add the spreadsheet ID to SPREADSHEETID in main.py  
    8.) Update the countries 2 letter characters in processor.py to match those of your spreadsheet. 
    9.) Run the main.py script. 

# Current_Bugs
    1.) Error when a country ID is entered with no number.  
    2.) Need to smooth out parsing and set a standard for messages.  

# Contributions
    Author: Jarod Klypchak -October 2018
