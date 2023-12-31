import pandas as pd


def update_status_file(ticker):
    status_file = "processing_status.csv"
    status_df = pd.read_csv(status_file)
    status_df.loc[status_df["ticker"] == ticker, "processed"] = True
    status_df.to_csv(status_file, index=False)
