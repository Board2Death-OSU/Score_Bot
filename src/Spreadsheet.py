from googleapiclient.discovery import build
import datetime
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES='https://www.googleapis.com/auth/spreadsheets'
class Spreadsheet:

    """
    History:
        3/26/19: Created and Implemented. -Jarod Klypchak
    Description:
        A constructor for this spreadsheet, opening it and ensuring user is authorized.
    Arguments:
        spreadsheet_id: the ID of the spreadsheet to be opened.
    Return:
        The new Spreadsheet object.
    """
    def __init__(self,spreadsheet_id):
        self.spreadsheet_id=spreadsheet_id
        store=file.Storage('../data/token.json')
        creds=store.get()
        if not creds or creds.invalid:
            flow=client.flow_from_clientsecrets('credentials.json',SCOPES)
            creds=tools.run_flow(flow,store)
        self.service=build('sheets','v4',http=creds.authorize(Http()))
    
    """
    History:
        3/26/19: Created and Implemented. -Jarod Klypchak
    Description:
        Reads the specified column/row from the specified page from this spreadsheet.
    Arguments:
        page: the page of the spreadsheet to extract data from.
        column: the specified column (a letter A-Z)
        row: the specified row (a numeric value)
    Return:
        A string containing the specified value.
    """
    def read_value(self,page,column,row):
        result=self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,range=(page+"!"+column+row)).execute()
        result=result.get('values',[])
        return result[0][0]

    """
    History:
        3/26/19: Created and Implemented. -Jarod Klypchak
    Description:
        Writes data the specified column/row from the specified page from this spreadsheet.
    Arguments:
        page: the page of the spreadsheet to write data to.
        column: the specified column (a letter A-Z)
        row: the specified row (a numeric value)
        value: the data to write to the cell.
    Return:
        None.
    """
    def write_value(self,page,column,row,value):
        dest=page+"!"+column+row
        values=[[value]]
        body={'values':values}
        result=self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,range=dest,valueInputOption="USER_ENTERED",body=body).execute()
        
    def find_empty_cell_in_column(self,page,column,row):
        search =page+"!"+column+row+":"+column
        result=self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,range=search).execute()
        current_row=0
        result=result.get('values',[])
        current_row+=int(row)+len(result)
        return current_row
    
    def write_row(self,page,column_start,column_end,row,data):
        location=page+"!"+column_start+row+":"+column_end+row
        values=[data]
        body={'values':values}
        self.service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id,range=location,valueInputOption="USER_ENTERED",body=body).execute()

    def read_column(self,page,column,row_start,row_end):
        location=page+"!"+column+row_start+":"+column+row_end
        result=self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,range=location).execute()
        result=result.get('values',[])
        values=[]
        for value in result:
            values.append(value[0])
        return values