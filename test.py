import pandas as pd
from local_utils import download_from_gsheets,download_from_gdrive, export_to_sheet

# link = "https://docs.google.com/spreadsheets/d/199H1tKkyCBVpnCVdfzI2D85DML9E9U_ePZuOua0D3gs/edit?usp=sharing"
df = pd.read_csv("results/full_top1000_links_apr2021.csv")
print(len(df))

# export_to_sheet(df,link,sheet_name="Sheet3")