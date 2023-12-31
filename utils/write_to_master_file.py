from filelock import FileLock


def write_to_master_file(master_df):
    with FileLock("all_ticker_10k_mda_data.csv.lock"):
        master_df.to_csv("all_ticker_10k_mda_data.csv", index=False)
