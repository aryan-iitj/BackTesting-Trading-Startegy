import numpy as np
import pandas as pd

def clean_price(p):
    """
    Read column of price strings to float
    Ex: "32,760" => 32760.0
    
    Parameters
    ----------
    p : str
        Price string "32,760"
    """
    return float(p.replace(',',''))

def read_bars(barpath):
    """
    Read OHCL bars from csv
    Note: Specific to csv's present in data folder

    Parameters
    ----------
    barpath : str
        Path to csv
    """
    df = pd.read_csv(barpath)
    df['Date'] = pd.to_datetime(df['Date'])
    for col in ['Open', 'High', 'Low', 'Close']:
        df[col] = df[col].apply(clean_price)
    df = df.sort_values('Date').reset_index(drop=True)
    return df

def run_backtest(df, algo, initial_val=10000, time_of_bar='Close'):
    """
    Execute a backtest with historical data and an algorithm
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns ['Date', 'Open', 'High', 'Close', 'Low']
        It is expected that the dataframe is sorted by 'Date' in inceasing order
        
    algo : tradingAlgo
        Trading algorithm to backtest
        
    Returns 
    ----------
    results : pd.DataFrame
        DataFrame with backtest results
    """
    
    # Initialize data structures
    n_shares = [0.0]
    asset_val = [0.0]
    cash_val = [initial_val]
    portfolio_val = [asset_val[-1] + cash_val[-1]]
    dates = [df.Date[0]]
    
    # Iterate through OHCL bars of data
    for i in range(1, len(df)):

        price = df.iloc[i][time_of_bar]
        
        # Find target allocation from algorithm
        target = algo.handle_data(df.iloc[:i])
        
        # Take on target position, record result
        if target == 0:
            cash_val.append((n_shares[-1]*price) + cash_val[-1])
            n_shares.append(0.0)
        elif target == 1:
            n_shares.append(n_shares[-1] + (cash_val[-1]/price))
            cash_val.append(0.0)
        else:
            raise ValueError("Target between (0,1) not supported yet!")
        
        asset_val.append(n_shares[-1] * price)
        portfolio_val.append(asset_val[-1] + cash_val[-1])
        dates.append(df.Date[i])
        
    return pd.DataFrame({'Date':dates, 'Cash Value':cash_val, 
                         'Asset Shares':n_shares, 'Asset Value':asset_val, 
                         'Portfolio Value':portfolio_val})