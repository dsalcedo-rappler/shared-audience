import pandas as pd

df = pd.read_csv("top1000_links_may2021.csv")

df2 = df[ (df['site1'] != "https://www.youtube.com/") & (df['link'] > 20) ]

df2.to_csv("sorted_top1000_links_apr2021.csv",index=False)