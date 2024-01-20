

from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns

from gen_sentiment_afinn import gen_sentiment_afinn
from gen_entities import gen_entities

def gen_stockdata(ticker, start_date, end_date, interval):
    # Retrieve tickers using yfinance
    tick = yf.Ticker(ticker)
    tick_hist = tick.history(start=start_date, end=end_date, interval=interval)
    
    # Get relative change
    tick_hist['Rel_change'] = tick_hist['Close'] - tick_hist['Open']

    return tick_hist

if __name__ == "__main__":
    ## Get sentiment related to GME
    sentiments = gen_sentiment_afinn()
    entities = gen_entities()

    # Find set of post_ids that have that entity
    post_ids = set()
    for (id, row) in entities.iterrows():
        post_id = row["post_id"]
        text = row["text"]
        
        if (text == "GME"):
            post_ids.add(post_id)

    # Filter sentiments by post id
    sentiments = sentiments.filter(items=post_ids, axis=0)

    # Aggregate sentiments over same day
    sentiments = sentiments.groupby(sentiments["created"].dt.date)["sentiment"].agg(["sum"])

    print(sentiments)

    ## Get price changes
    tick_hist = gen_stockdata("GME", "2021-01-01", "2021-04-01", "1d")

    ## Plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=tick_hist, x='Date', y='Rel_change', label='GME price change', color='b')
    sns.lineplot(data=sentiments, x='created', y='sum', label='GME sentiment', color='r')
    plt.xlabel('Date')
    plt.title('GME price change')
    plt.legend()
    plt.show()

