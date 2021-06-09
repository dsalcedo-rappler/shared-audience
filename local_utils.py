
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