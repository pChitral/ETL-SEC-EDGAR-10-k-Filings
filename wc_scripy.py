import pandas as pd
from utils.process_ticker_10k_data import process_ticker_10k_data


df = pd.read_json("company_tickers.json", orient="index")

all_tickers_data = {}
tickers = df["ticker"].tolist()

count = 0
for ticker in tickers:
    all_tickers_data[ticker] = process_ticker_10k_data(ticker)
    count += 1
    if count > 100:
        break
