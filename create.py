"""
Creates a csv for used to generate the network
"""

import time
import pandas as pd
import itertools
from local_utils import get_agents, shared_audience, download_from_gsheets, download_from_gdrive, export_to_sheet

tstart = time.perf_counter()

## Import posts

# Use this if you want to use local files
# input_file_posts = "data/sharktank-db-202104.csv"
# df = pd.read_csv(input_file_posts)

# Use this if you want to get files from gdrive
input_file_posts_link = "https://drive.google.com/file/d/1sE5NLYbI8NP2-00GQCTwm4bFWF0IwteR/view?usp=sharing"
input_file_posts = download_from_gdrive(input_file_posts_link)
df = pd.read_csv("Filename.csv")



## Import pages

# Use this if you want to use local files
# input_file_pages = "data/channels_202104_test.csv"
# top = pd.read_csv(input_file_pages).head(1000)

# Use this if you want to get files from gdrive
input_file_pages_link = "https://docs.google.com/spreadsheets/d/1BLgcBfCWGbcycftwwnvb2WAtGKn42hUat_69gX1YElI/edit?usp=sharing"
input_file_pages = download_from_gsheets(input_file_pages_link,sheet='channels_202104')
top = input_file_pages.head(1000)
top['linkEntityId'] = top['linkEntityId'].astype(int)


## Define outputs
output_file = "results/top1000_links_202104.csv"
# output_link = "https://docs.google.com/spreadsheets/d/1YySi80E3PstrXZF_YKigKRg0RO76MocS-dOAuOiDjmg/edit?usp=sharing"


# Code proper
df2 = df[~df['linkWebsite'].isna()]
pages_df = top
num_pages = 1000

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
            "site1": pages_df.loc[pair[0],'linkEntityId'],
            "site2": pages_df.loc[pair[1],'linkEntityId'],
            "link": res['commons']
        })
    counter+= 1
    if counter%100 == 0:
        print(f"Processed {counter} of {total_pairs} pairs")
    if counter == total_pairs:
        print(f"Processed {counter} of {total_pairs} pairs")

links = pd.DataFrame(links)
links.to_csv(output_file,index=False)
links2 = pd.read_csv(output_file)
# export_to_sheet(links2,output_link,sheet_name="top_all")

tend = time.perf_counter()
print(f"Time elapsed: {tend-tstart}")