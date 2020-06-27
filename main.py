# Using the API: https://github.com/statsbomb/statsbombpy
# Stats from StatsBomb free datasets

import pandas as pd
from pandas import json_normalize
import json
import requests
from tqdm.auto import tqdm

# Github root url for statsbomb data.
stats_bomb_url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/'

# Todo Get all the data which feature Barcalona from the statsbomb 'Matches'

def FreeMatches(competitions):
    """
    Function to get all the free matches from Stats bomb github free data.

    Args:
        'competitions' given as a dataframe must contain 'competition_id' and 'season_id'

    Returns:
        matches_dataframe (DataFrame): Return a dataframe with all the Free Matches with 'competition_id' & 'season_id'
    """

    matches_dataframe = pd.DataFrame()

    for i in tqdm(range(len(competitions))):
        comp_id = str(competitions['competition_id'][i])
        season_id = str(competitions['season_id'][i])

        matches_url = stats_bomb_url+f"matches/{comp_id}/{season_id}.json"

        raw_matches = requests.get(url=matches_url)
        matches = json_normalize(raw_matches.json())
        matches_dataframe = matches_dataframe.append(matches, ignore_index=True, sort=False)

        return matches_dataframe

