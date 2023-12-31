import os
import pandas as pd


def initialize_status_file(df):
    status_file = "processing_status.csv"
    if not os.path.exists(status_file):
        status_df = pd.DataFrame({"ticker": df["ticker"], "processed": False})
        status_df.to_csv(status_file, index=False)
