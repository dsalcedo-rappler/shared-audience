"""
Creates a csv for used to generate the network
"""

import time
import pandas as pd
import itertools
from local_utils import get_agents, shared_audience, download_from_gsheets, download_from_gdrive, export_to_sheet

tstart = time.perf_counter()
# Import posts
# input_file_posts = "data/sharktank-db-202104.csv"
# df = pd.read_csv(input_file_posts)
input_file_posts_link = "https://drive.google.com/file/d/1sE5NLYbI8NP2-00GQCTwm4bFWF0IwteR/view?usp=sharing"
input_file_posts = download_from_gdrive(input_file_posts_link)
df = pd.read_csv("Filename.csv")

# Import pages
# input_file_pages = "data/channels_202104_test.csv"
# top100 = pd.read_csv(input_file_pages).head(100)
input_file_pages_link = "https://docs.google.com/spreadsheets/d/1nVPbm98ZZCpbVF0vluvHxEPftz4lUtnAb9CZv0EF9ew/edit?usp=sharing"
input_file_pages = download_from_gsheets(input_file_pages_link,sheet='channels_202104')
top100 = input_file_pages.head(100)
top100['linkEntityId'] = top100['linkEntityId'].astype(int)

# output_file = "results/top100_links_apr2021_test.csv"
output_link = "https://docs.google.com/spreadsheets/d/199H1tKkyCBVpnCVdfzI2D85DML9E9U_ePZuOua0D3gs/edit?usp=sharing"

df2 = df[~df['linkWebsite'].isna()]
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
# links.to_csv(output_file,index=False)
export_to_sheet(links,output_link,sheet_name="top100")

tend = time.perf_counter()
print(f"Time elapsed: {tend-tstart}")