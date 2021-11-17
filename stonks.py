import openpyxl, pyodbc
import win32com.client
from config import PORTFOLIO_WB
from openpyxl import Workbook
from datetime import datetime

"""
    Tracks my stock portfolio performance in a local SQL database
"""

def newDBEntry(date, value, cursor, cnxn):
    """Add new entry in the DB for the current value of the portfolio
    params
        date: datetime - today's date
        value: float - current value of portfolio from excel file
    return
        resulting message
    """
    try:
        cursor.execute("INSERT INTO GROWTH_T (Date, Total_Value) VALUES ('{}', '{}');".format(date, value)) 
        cnxn.commit()                        
        return 'New entry has been created.'
    except:
        return 'Error! Something went wrong when adding this entry...'

def refreshExcel(excel_wb):
    """ refreshes all the data connections in an excel workbook and then saves it

    Params
    ------
        excel_wb: workbook obj - excel file containing portfolio information
    """
    # refresh excel data connection
    xlapp = win32com.client.DispatchEx("Excel.Application")
    wb = xlapp.Workbooks.Open(excel_wb)
    wb.RefreshAll()
    xlapp.CalculateUntilAsyncQueriesDone()
    wb.Save()
    xlapp.Quit()

def getPortValue(excel_wb):
    """ opens a given excel workbook and retrieves the value from a specific cell

    Params
    ------
        excel_wb: workbook obj - excel file containing portfolio information
    Returns
    ------
        port_value: float - current portfolio total
    """
    # open workwook and get portfolio value
    wb = openpyxl.load_workbook(excel_wb, data_only=True)
    portfolio = wb.worksheets[0]
    port_value = portfolio['F9'].value
    print(f"Today's Portfolio Close: ${round(port_value,2)}")
    wb.close()
    return port_value

def getTodayDate():
    """ Get's the current date and time and converts it to a string
    
    Returns
    -------
        current_datetime: string - current datetime
    """
    current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    print(f"Today's datetime: {current_datetime}")
    return current_datetime

if __name__ == '__main__':
    
    # SQLconfig
    SERVER = 'localhost\SQLEXPRESS'
    DATABASE = 'Stonks' 
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';Trusted_Connection=yes;')
    cursor = cnxn.cursor()
    
    current_datetime = getTodayDate()

    refreshExcel(PORTFOLIO_WB)
    port_value = getPortValue(PORTFOLIO_WB)
    message = newDBEntry(current_datetime, port_value, cursor, cnxn)

    print(message)