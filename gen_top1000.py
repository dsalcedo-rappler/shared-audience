"""
Generates the top 100 shared channels to be used for a BigQuery job
"""

import pandas as pd

input_file = "data/sharktank-db-201810.csv"
output_file = "results/top1000_channels_201810.csv"

df = pd.read_csv(input_file)
df2 = df[~df['linkWebsite'].isna()]

df3 = (
    df2
    .groupby(['linkEntityId','linkWebsite','linkType'],as_index=False)
    .agg(shares=('linkWebsite','count'))
    .sort_values('shares',ascending=False)
    .reset_index(drop=True)
    .rename(columns={'linkType':'channelType'})
    .astype({'linkEntityId': 'int'})
    .head(1000)
)

df3.to_csv(output_file,index=False)