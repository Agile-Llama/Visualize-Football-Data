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


def FreeCompeitions():
    """
    Function to get all the Free Competitions from StatsBomb free dataset.

    Returns:
        compeitions_dataframe (dataframe): Return a DataFrame with all the Free Competitions.
    """

    competitions_url = stats_bomb_url + "competitions.json"
    raw_competitions = requests.get(url=competitions_url)
    raw_competitions.encoding = 'utf-8'
    competitions = raw_competitions.json()

    compeitions_dataframe = pd.DataFrame(competitions)
    return compeitions_dataframe


# Works well with 'FreeCompeitions"
def FreeMatches(competitions):
    """
    Function to get all the free matches from StatsBomb free dataset.

    Args:
        'competitions' (DataFrame) : Must contain 'competition_id' and 'season_id'

    Returns:
        matches_dataframe (DataFrame): Return a dataframe with all the Free Matches.
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


def MatchEvents(match_id):
    """
    Function to get all the all the events from a Match

    Args:
        match_id (int) : id of the game to get the events of

    Returns:
        match_events_dataframe (DataFrame): Return a dataframe with all the Events from a Match.
    """

    events_url = stats_bomb_url + f"events/{match_id}.json"
    raw_events_api = requests.get(url=events_url)
    raw_events_api.encoding = 'utf-8'
    events = pd.DataFrame(json_normalize(raw_events_api.json()))

    events.loc[:, 'match_id'] = match_id
    return events





