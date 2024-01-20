

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns

def gen_stockdata(ticker, start_date, end_date, interval):
    # Retrieve tickers using yfinance
    tick = yf.Ticker(ticker)
    tick_hist = tick.history(start=start_date, end=end_date, interval=interval)
    sp500 = yf.Ticker("^GSPC")
    sp500_hist = sp500.history(start=start_date, end=end_date, interval=interval)

    print(sp500_hist)
    
    # Get relative change
    tick_hist['Rel_change'] = np.log(tick_hist['Close']) - np.log(tick_hist['Open'])
    sp500_hist['Rel_change'] = np.log(sp500_hist['Close']) - np.log(sp500_hist['Open'])

    # Get relative change to SP500
    tick_hist["Rel_change_SP500"] = tick_hist["Rel_change"] - sp500_hist["Rel_change"]

    print(tick_hist)

    return tick_hist

if __name__ == "__main__":
    tick_hist = gen_stockdata("GME", "2021-01-01", "2021-04-01", "1d")

    # Display both relative change of GME and relative change to SP500 of GME.
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=tick_hist, x='Date', y='Rel_change', label='GME change', color='b')
    sns.lineplot(data=tick_hist, x='Date', y='Rel_change_SP500', label='GME rel. change to SP500', color='r')
    plt.xlabel('Date')
    plt.title('GME price change')
    plt.legend()
    plt.show()

