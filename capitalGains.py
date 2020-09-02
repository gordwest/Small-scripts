import pandas as pd
import datetime

# get list of stocks that you sold during the year
def getSoldStocks(trxns):
    """ returns a list of stocks that were sold in the current year
    params
        trxns: dataframe - table of transactions read from an excel file
        date: datetime - year to be calculating gains/losses for 
    """
    sold = trxns[(trxns['Action'] == 'Sell') & (trxns['Date'] > pd.to_datetime('2019-12-31'))]
    return sold['Stock'].unique()

def currentStatus(shares_held, position, rollingPrice, profit):
    """ Returns the appropriate update message after processing a new transaction
    shares_held: int - number of shares held after the transaction
    position: float - total amount of money in the current position
    rollingPrice: float - average price per share as transactions occur
    profit - accumulating profit as after transactions occur
    """
    if shares_held == 0:
        return '    Current Shares:{:<10} Position:${:<13} Rolling Price:${:<10} Gains/Loss:${:<10}'.format(shares_held, 0, rollingPrice, profit)
    else:
        return '    Current Shares:{:<10} Position:${:<13} Rolling Price:${:<10} Gains/Loss:${:<10}'.format(shares_held, position, rollingPrice, profit)

def stockRecap(shares_sold, shares_held, position, price, profit):
    """ Returns the appropriate update message after processing all transactions for a given stock
    shares_sold: int - total number of shares sold
    shares_held: int - number of shares held after the transaction
    position: float - total amount of money in the current position
    price: float - average price the shares were sold at for a profit
    profit - total gains/loss after all transactions
    """
    print('-----------------------------------------------------------------------------------------------')
    if shares_held == 0:
        return '    Total Shares Sold:{:<7} Position:${:<13} Price/Share:${:<12} Gains/Loss:${:<10}\n'.format(shares_sold, 0, price, profit)
    else:
        return '    Total Shares Sold:{:<7} Position:${:<13} Price/Share:${:<12} Gains/Loss:${:<10}\n'.format(shares_sold, position, price, profit)

def capitalGainsLoss(net_profit):
    """ Returns the appropriate message based on whether gains or losses occured
    net_profit: float - total gains/loss between all transactions
    """
    if net_profit > 0:
        return 'You need to claim taxes on ${} (plus dividends)'.format(round(net_profit,2))
    else:
        return 'You can claim ${} worth of losses'.format(round(net_profit,2))


def main():
    # read stock transactions
    trxns = pd.read_excel('C:/Users/gordi/Desktop/Documents/Stock Transactions.xlsx', 'Sheet1')
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

            print(currentStatus(shares_held, round(position,2), round(rollingPrice,2), round(profit,2))) # get update after every transaction

        net_profit += profit # keep track of profit across all stocks
        print(stockRecap(shares_sold, shares_held, round(position,2), round(trxns_subset.loc[i, 'Price (CAD)'],2), round(profit,2)))
    print(capitalGainsLoss(net_profit)) # print gains/loss
    
if __name__ == "__main__":
    main()
