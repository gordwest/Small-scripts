import cv2, pytesseract
from PIL import Image
import pandas as pd
from datetime import date, timedelta, datetime

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def dividends(img_path):
    img = cv2.imread(img_path)
    raw_text = pytesseract.image_to_string(img)
    text_arr = raw_text.strip().splitlines()
    payments = [float(line.replace('$', '')) for line in raw_text.split('\n') if line.strip() != '']
    return round(sum(payments),2)

def getTimeFrame(year):
    nextYear = (datetime.strptime(year, '%Y') + timedelta(weeks=52+1)).strftime("%Y")
    startDate = datetime.strptime('{}-{}-{}'.format(year, '01', '01'), '%Y-%m-%d')
    endDate = datetime.strptime('{}-{}-{}'.format(nextYear, '01', '01'), '%Y-%m-%d')
    return startDate, endDate

# get list of stocks that you sold during the year
def getSoldStocks(trxns, startDate, endDate):
    """ returns a list of stocks that were sold in the current year
    params
        trxns: dataframe - table of transactions read from an excel file
        date: datetime - year to be calculating gains/losses for 
    """
    sold = trxns[(trxns['Action'] == 'Sell') & (trxns['Date'] < endDate) & (trxns['Date'] >= startDate)]
    return sold['Stock'].unique()

def currentStatus(action, shares_held, position, rollingPrice, profit):
    """ Returns the appropriate update message after processing a new transaction
    shares_held: int - number of shares held after the transaction
    params
        position: float - total amount of money in the current position
        rollingPrice: float - average price per share as transactions occur
        profit - accumulating profit as after transactions occur
    """
    if shares_held == 0:
        return '\t{:<5}\t      {:<10}  ${:<10}    ${:<10}\t${:<10}'.format(action, int(shares_held), 0, rollingPrice, profit)
    else:
        return '\t{:<5}\t      {:<10}  ${:<10}    ${:<10}\t${:<10}'.format(action, int(shares_held), position, rollingPrice, profit)

def stockRecap(shares_sold, price, profit):
    """ Returns the appropriate update message after processing all transactions for a given stock
    params
        shares_sold: int - total number of shares sold
        price: float - average price the shares were sold at for a profit
        profit - total gains/loss after all transactions
    """
    print('\t-----------------------------------------------------------------')
    # return '     Sold\t    {:<7}\t   ${:<10}   ${:<10}\t${:<10}\n'.format(shares_sold, round(shares_sold*price,2), price, profit)
    return '\tSold {} shares at ${} (${}) for a total gain/loss of ${}\n'.format(int(shares_sold), price, round(shares_sold*price,2), profit)

def capitalGainsLoss(net_profit):
    """ Returns the appropriate message based on whether gains or losses occured
    net_profit: float - total gains/loss between all transactions
    """
    if net_profit >= 0:
        return 'You need to claim taxes on ${} (plus dividends)'.format(round(net_profit,2))
    else:
        return 'You can claim ${} worth of losses'.format(abs(round(net_profit,2)))


def main():

    # defines the year to calc for
    year = '2020'
    startDate, endDate = getTimeFrame(year)

    # read stock transactions
    trxns = pd.read_excel('C:/Users/gordi/Desktop/Documents/Stock Transactions.xlsx', 'Transactions')
    trxns['Date'] = trxns['Date'].astype('datetime64[ns]')
    soldStocks = getSoldStocks(trxns, startDate, endDate) # get list of stocks that were sold

    net_profit = 0 # initalize variable for net gains/losses
    for stock in soldStocks:
        shares_held, shares_sold, position, rollingPrice, profit = 0, 0, 0, 0, 0 # initialize variables for current stock
        trxns_subset = trxns[trxns['Stock'] == stock].reset_index() # subset transactions for given stock
        print(stock) # print line for spacing
        print('\tAction\t Share Balance\t  Position\tAvg Price\tGains/Loss')
        print('\t-----------------------------------------------------------------')
        for i in range(0, len(trxns_subset)): # loop through transactions records
            if trxns_subset.loc[i, 'Action'] == 'Buy': # update position and rolling share price when buying
                shares_held += trxns_subset.loc[i, 'Shares']
                position += trxns_subset.loc[i, 'Total']
                rollingPrice = position / shares_held
            else: # update position and rolling share price when selling
                if trxns_subset.loc[i, 'Date'] < startDate:
                    shares_held -= trxns_subset.loc[i, 'Shares']
                    position -= trxns_subset.loc[i, 'Total']
                else: # selling shares for gains/losses
                    shares_sold += trxns_subset.loc[i, 'Shares']
                    shares_held -= trxns_subset.loc[i, 'Shares']
                    position -= trxns_subset.loc[i, 'Total']
                    profit += (trxns_subset.loc[i, 'Price (CAD)'] - rollingPrice) * trxns_subset.loc[i, 'Shares']

            print(currentStatus(trxns_subset.loc[i, 'Action'], shares_held, round(position,2), round(rollingPrice,2), round(profit,2))) # get update after every transaction

        net_profit += profit # keep track of profit across all stocks
        print(stockRecap(shares_sold, round(trxns_subset.loc[i, 'Price (CAD)'],2), round(profit,2)))
    print(capitalGainsLoss(net_profit) + ' for ' + year + '.\n') # print gains/loss

    # add up dividend payments from image
    print('${} of dividends were colleted in {}!'.format(dividends('C:/Users/gordi/Desktop/Dividends.png'), year))
    
if __name__ == "__main__":
    main()