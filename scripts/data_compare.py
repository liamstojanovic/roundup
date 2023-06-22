# data_compare.py
# Lorae Stojanovic
# Special thanks to ChatGPT for coding assistance in this project.
# LE: 22 Jun 2023

import pandas as pd
import os

# hist_path is an argument representing where the historical comparison data is
# located. recent_path is an argument representing where the newest data is
# located. Both must be .json files for the code to work.
def compare_new_data(hist_path, recent_path):
    # Ensure the historical and recent files exist
    if not os.path.exists(hist_path) or not os.path.exists(recent_path):
        print(f"One or both of the files {hist_path}, {recent_path} do not exist")
        return

    # Load historical and recent data
    hist_df = pd.read_json(hist_path)
    recent_df = pd.read_json(recent_path)

    # Ensure the necessary columns exist
    for column in ["Number", "Link"]:
        if column not in hist_df.columns or column not in recent_df.columns:
            print(f"The column {column} is not in one or both of the dataframes")
            return

    # Identify new data
    merged_df = pd.merge(hist_df, recent_df, how='outer', indicator=True)
    new_df = merged_df.loc[merged_df._merge == 'right_only', :]

    # If "Number" and "Link" are missing in the new data, raise an error
    if new_df[["Number", "Link"]].isnull().all(axis=1).any():
        raise ValueError("Both 'Number' and 'Link' are missing for some entries in the new data")

    # Save new data to a json file
    new_df.to_json("new_data/test_new.json", orient='records')
    print(f"New data saved to test_new.json")
