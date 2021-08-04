import pandas as pd

df = pd.read_csv("results/full_top1000_links_apr2021.csv")

# df2 = df[ (df['site1'] != "https://www.youtube.com/") & (df['link'] > 20) ]
df2 = df[ df['link'] >= 5 ]

df2.to_csv("results/sorted_top1000_links_apr2021_05up.csv",index=False)