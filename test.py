from local_utils import download_from_gsheets, export_to_sheet

link = "https://docs.google.com/spreadsheets/d/1z4huRRB0WUre_7CmJl_38KKdJ3y_GoLXPh9NP37l2BQ/edit?usp=sharing"
df = download_from_gsheets(link,sheet="posts")

export_to_sheet(df,link,sheet_name="posts2")