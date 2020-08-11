import pandas as pd
import datetime

trxns = pd.read_excel('C:/Users/gordi/Desktop/Documents/Stock Transactions.xlsx', 'Sheet1')
print(trxns.head())
print()

# get list of stocks that you sold during the year
def getSoldStocks(trxns):
    """ returns a list of stocks that were sold in the current year
    params
        trxns: dataframe - table of transactions read from an excel file
        date: datetime - year to be calculating gains/losses for 
    """
    sold = trxns[(trxns['Action'] == 'Sell') & (trxns['Date'] > pd.to_datetime('2019-12-31'))]
    return sold['Stock'].unique()

def main():
    soldStocks = getSoldStocks(trxns) # get list of stocks that were sold
    net_profit = 0 # initalize variable for net gains/losses
    for stock in soldStocks:
        shares_held, shares_sold, position, rollingPrice, profit = 0, 0, 0, 0, 0 # initialize variables for current stock
        trxns_subset = trxns[trxns['Stock'] == stock].reset_index() # subset transactions for given stock
        print(stock) # print line for spacing
        for i in range(0, len(trxns_subset)): # loop through transactions records
            if trxns_subset.loc[i, 'Action'] == 'Buy': # update position and rolling share price when buying
                shares_held += trxns_subset.loc[i, 'Shares']
                position += trxns_subset.loc[i, 'Total']
                rollingPrice = position / shares_held
            else: # update position and rolling share price when selling
                if trxns_subset.loc[i, 'Date'] < pd.to_datetime('2020-01-01'):
                    shares_held -= trxns_subset.loc[i, 'Shares']
                    position -= trxns_subset.loc[i, 'Total']
                else: # selling shares for gains/losses
                    shares_sold += trxns_subset.loc[i, 'Shares']
                    shares_held -= trxns_subset.loc[i, 'Shares']
                    position -= trxns_subset.loc[i, 'Total']
                    profit += (trxns_subset.loc[i, 'Price (CAD)'] - rollingPrice) * trxns_subset.loc[i, 'Shares']
            print('Current Shares:{} Position:{} Rolling Price:${} Profit:${}'.format(shares_held, position, rollingPrice, profit)) # update current status of stock after transaction
        net_profit += profit # keep track of profit across all stocks
        print('Shares sold:{} Price:${} Profit:${}'.format(shares_sold, trxns_subset.loc[i, 'Price (CAD)'], profit)) # declare the gains/losses for the given stock
        print('')

    print('You need to claim taxes on ${} (plus dividends)'.format(net_profit)) # total all gains/losses for all stocks
    
if __name__ == "__main__":
    main()
