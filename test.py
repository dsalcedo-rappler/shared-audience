from local_utils import download_from_gsheets,download_from_gdrive, export_to_sheet

link = "https://docs.google.com/spreadsheets/d/1z4huRRB0WUre_7CmJl_38KKdJ3y_GoLXPh9NP37l2BQ/edit?usp=sharing"
df = download_from_gsheets(link,sheet="posts")

print("downloading")
link2 = "https://drive.google.com/file/d/1A-ZV14ixqjNzgsF0I8HpVO3NBJytzuZ_/view?usp=sharing"
df2 = download_from_gdrive(link2,colab_filename="Filename.csv")

print("done")
export_to_sheet(df,link,sheet_name="posts2")