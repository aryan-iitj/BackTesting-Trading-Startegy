import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

import utils as utils
from tradingAlgo import tradingAlgo

class dualMovingAverageCrossover(tradingAlgo):
    """
    Dual Moving Average Crossover trading algorithm 
    
    Handles only 1 price ticker. Utilizes a short term simple
    moving average and a long term simple moving average to 
    define bullish/bearish trend.
    """
    
    def __init__(self, short_lookback, long_lookback, time_of_bar='Close'):
        """
        Initialize an instance of class dualMovingAverageCrossover
        by specifying algorithm hyperparameters
        
        Parameters
        ----------
        short_lookback : int
            Number of bars to lookback for short term moving average
            
        long_lookback : int
            Number of bars to lookback for long term moving average
            
        time_of_bar : str from ['Open', 'High', 'Low', 'Close']
            Time of OHCL bar data to use for indicators
        """
        
        self._short_lookback = short_lookback
        self._long_lookback = long_lookback
        self._time_of_bar = time_of_bar
    
    def handle_data(self, data):
        """
        Called every time a bar of data is pushed from the backtesting
        or live trading API
        
        Parameters
        ----------
        data : pd.DataFrame
            OHCL price bars for the asset(s) of choice
        """
        
        px = data[self._time_of_bar].values
        if len(px) < self._long_lookback + 1:
            return 0
        signal = self._generate_signal(px)
        target = signal * 1.0
        return target
    
    def _generate_signal(self, px):
        """
        Generate trading signal given price data
        """
        
        sma = px[-self._short_lookback:].mean()
        lma = px[-self._long_lookback:].mean()
        if sma > lma:
            return 1
        else:
            return 0


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage:")
        print("    python3 dualMovingAverageCrossover.py short_lookback long_lookback")
        print("    Ex: python3 dualMovingAverageCrossover.py 20 50")
    
    short_lookback = int(sys.argv[1])
    long_lookback = int(sys.argv[2])
    
    dma_crossover = dualMovingAverageCrossover(short_lookback, long_lookback)

    # BTC backtest
    df_btc = utils.read_bars("data/BTCUSD_daily_bars.csv")
    result_btc = utils.run_backtest(df_btc, dma_crossover)
    result_btc['Percent Change'] = result_btc['Portfolio Value'].apply(lambda x: 100 * x / result_btc['Portfolio Value'].iloc[0])
    print("BTC backtest complete")

    # ETH backtest
    df_eth = utils.read_bars("data/ETHUSD_daily_bars.csv")
    result_eth = utils.run_backtest(df_eth, dma_crossover)
    result_eth['Percent Change'] = result_eth['Portfolio Value'].apply(lambda x: 100 * x / result_eth['Portfolio Value'].iloc[0])
    print("ETH backtest complete")

    # Plot percent change
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.plot(result_btc['Date'], result_btc['Percent Change'], label="BTC")
    ax.plot(result_eth['Date'], result_eth['Percent Change'], label="ETH")
    ax.legend(fontsize='large')
    ax.set_xlabel("Date", fontsize='large')
    ax.set_ylabel("Percentage Change (%)", fontsize='large')
    ax.set_title("Dual Moving Average Crossover (20d, 50d) BTC vs. ETH", fontsize='large')
    plot_title = "dualMovingAverageCrossover({}, {})_BTC_ETH.png".format(short_lookback, long_lookback)
    fig.savefig(plot_title)
    print("Output plot saved to {}".format(plot_title))