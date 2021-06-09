"""
Creates a csv for used to generate the network
"""

import time
import pandas as pd
import itertools

tstart = time.perf_counter()

df = pd.read_csv("data/sharktank-db-202104.csv")
df2 = df[~df['linkWebsite'].isna()]

top100 = pd.read_csv("data/channels_202104_test.csv")

def get_agents(pages,posts,index):
    """
    Return the unique agents of a certain channel as a set list
    """
    site = pages.loc[index]
    agents = posts[ (posts['linkEntityId'] == site['linkEntityId']) & (posts['linkType'] == site['channelType']) ]['fromProfile']
    return set(list(agents))

def shared_audience(pages,posts,site_ind1,site_ind2,threshold=0):
    """
    Returns the if two channels have a shared audience greater than the threshold,
    as well as how many common agents they have
    """
    agents1 = get_agents(pages,posts,site_ind1)
    agents2 = get_agents(pages,posts,site_ind2)
    common_agents = agents1.intersection(agents2)

    if len(common_agents) >= threshold:
        return {"shared": True, "commons": len(common_agents) }
    else:
        return {"shared": False, "commons": len(common_agents) }

#53 for yt, 0 for nonYt
# shared_audience(top100,df2,0,53)

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
links.to_csv("results/top100_links_apr2021_test.csv",index=False)

tend = time.perf_counter()
print(f"Time elapsed: {tend-tstart}")