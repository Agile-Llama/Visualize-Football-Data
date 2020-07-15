# Stats from StatsBomb free datasets. Gets from github

import pandas as pd
from pandas import json_normalize
import json
import requests
from tqdm.auto import tqdm

# Github root url for statsbomb data.
stats_bomb_url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/'



# Start with getting all the stats from statsbomb github. 


def FreeCompetitions():
    """
    Function to get all the Free Competitions from StatsBomb free dataset.

    Returns:
        competitions_dataframe (dataframe): Return a DataFrame with all the Free Competitions.
    """

    competitions_url = stats_bomb_url + "competitions.json"
    raw_competitions = requests.get(url=competitions_url)
    raw_competitions.encoding = 'utf-8'
    competitions = raw_competitions.json()

    competitions_dataframe = pd.DataFrame(competitions)
    return competitions_dataframe


# Works well with 'FreeCompetitions"
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


def get_match_free(match_id):
    """Function to get all the all the events from a Match

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


# Data from a list of matches (use get_matchFree)
def StatsBombFreeEvents(matchesdf):
    """Function to create DataFrame with events from match.

        Args:
            matchesdf (DataFrame): dataframe of matches. Must have columns 'match_id', 'competition_id', and 'season_id'.
    
        Returns:
            df (DataFrame): DataFrame with all events from all matches.

    """
    res = []
    for ind in tqdm(matchesdf.index):
        events = get_match_free(matchesdf[matchesdf.index == ind]['match_id'].values[0])
        events.loc[:, 'competition_id'] = matchesdf[matchesdf.index == ind]['competition.competition_id'].values[0]
        events.loc[:, 'season_id'] = matchesdf[matchesdf.index == ind]['season.season_id'].values[0]
        res.append(events)
    df = pd.concat(res, sort=True)
    return df


def get_lineups(match_id):
    """ Function which gets the lineup from a given match id.

    Args:
        match_id (int) : id of the game

    Returns:
        events (DataFrame): DataFrame with all events.

    """

    events_url = stats_bomb_url+"lineups/{match_id}.json"
    events_api = requests.get(url=events_url)
    events_api.encoding = 'utf-8'
    events = pd.DataFrame(json_normalize(events_api.json(), 'lineup', ['team_id', 'team_name']))
    
    events.loc[:, 'match_id'] = match_id

    return events


def StatsBombFreelineups(matches_dataframe):
    """Function to create DataFrame with events from match.

        Args:
            matches_dataframe (DataFrame): dataframe of matches. This must include 'match_id', 'competition_id', and 'season_id'.

        Returns:
            dataframe (DataFrame): DataFrame with all events from all matches.

    """
    res = []
    for ind in matches_dataframe.index:
        events = get_lineups(matches_dataframe[matches_dataframe.index == ind]['match_id'].values[0])
        events.loc[:, 'competition_id'] = matches_dataframe[matches_dataframe.index == ind]['competition.competition_id'].values[0]
        events.loc[:, 'season_id'] = matches_dataframe[matches_dataframe.index == ind]['season.season_id'].values[0]
        res.append(events)
    dataframe = pd.concat(res, sort=True)
    return dataframe


# Next set of functions will be to do with drawing the football pitch and other things like heatmaps, passmaps etc...

