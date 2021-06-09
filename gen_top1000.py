"""
Generates the top 100 shared channels to be used for a BigQuery job
"""

import pandas as pd

input_file = "data/sharktank-db-201810.csv"
output_file = "results/top1000_channels_oct2018.csv"

df = pd.read_csv(input_file)
df2 = df[~df['linkWebsite'].isna()]

df3 = df2.groupby(['linkEntityId','linkType'],as_index=False).agg(shares=('linkWebsite','count')).sort_values('shares',ascending=False).reset_index(drop=True)
df3 = df3.rename(columns={'linkType':'channelType'})

top = df3.head(1000)
top['linkEntityId'] = top['linkEntityId'].astype(int)

top.to_csv(output_file,index=False)