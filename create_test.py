"""
Creates a csv for used to generate the network
"""

import time
import pandas as pd
import itertools
from local_utils import get_agents, shared_audience

tstart = time.perf_counter()
input_file_posts = "data/sharktank-db-202104.csv"
input_file_pages = "data/channels_202104_test.csv"
output_file = "results/top100_links_apr2021_test.csv"

df = pd.read_csv(input_file_posts)
df2 = df[~df['linkWebsite'].isna()]

top100 = pd.read_csv(input_file_pages)
top100 = top100.head(100)

pages_df = top100
num_pages = 100

links = []
commons = []
page_inds = pages_df.index.tolist()
pairs = list(itertools.combinations(page_inds,2))
counter = 0
total_pairs = num_pages*(num_pages-1)/2
for pair in pairs:
    res = shared_audience(pages=pages_df,posts=df2,site_ind1=pair[0],site_ind2=pair[1])
    link = res['shared']
    commons.append(res['commons'])
    if link == True:
        links.append({
            "site1": pages_df.loc[pair[0],'channelName'],
            "site2": pages_df.loc[pair[1],'channelName'],
            "link": res['commons']
        })
    counter+= 1
    if counter%100 == 0:
        print(f"Processed {counter} of {total_pairs} pairs")
    if counter == total_pairs:
        print(f"Processed {counter} of {total_pairs} pairs")

links = pd.DataFrame(links)
links.to_csv(output_file,index=False)

tend = time.perf_counter()
print(f"Time elapsed: {tend-tstart}")