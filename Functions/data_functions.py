import sys

import pandas as pd

from pandas import json_normalize
import json
from tqdm.auto import tqdm

import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import numpy as np
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter

import requests

from matplotlib.colors import Normalize
import matplotlib.patheffects as pe

import config

from ast import literal_eval

plt.style.use('fivethirtyeight')

sys.path.insert(0, '../')


# Function to retrieve free competitions from StatsBomb open data
# comp_df (dataframe): DataFrame with all free competitions.
def FreeCompetitions(env='local'):
    competitions_path = config.data_dir + 'competitions.json'
    with open(competitions_path, encoding='utf-8') as json_file:
        competitions = json.load(json_file)

    comp_df = pd.DataFrame(competitions)
    return comp_df


# Function to retrieve matches from all competitions in competitions
# Args: competitions (DataFrame): df with competitions, must contain 'competition_id' and 'season_id'
def FreeMatches(competitions, env='local'):
    matches_df = pd.DataFrame()
    
    for i in tqdm(range(len(competitions))):
        comp_id = str(competitions['competition_id'][i])
        season_id = str(competitions['season_id'][i])
        matches_url = config.data_dir + \
                f"/matches/{comp_id}/{season_id}.json"

        with open(matches_url, encoding='utf-8') as json_file:
            raw_matches = json.load(json_file)
            matches = json_normalize(raw_matches)
            matches_df = matches_df.append(matches, ignore_index=True, sort=False)

    return matches_df


# Function to retrieve events from a match.
# Returns events (DataFrame): DataFrame with all events.
def get_matchFree(match_id, env='loval'):

    events_url = config.data_dir + f"events/{match_id}.json"
    with open(events_url, encoding='utf-8') as json_file:
        raw_events_api = json.load(json_file)
    events = pd.DataFrame(json_normalize(raw_events_api))
    events.loc[:, 'match_id'] = match_id
    return events


# Function to create DataFrame with events from match
# Returns: df (DataFrame): DataFrame with all events from all matches.
def StatsBombFreeEvents(matchesdf, env='local'):
    res = []
    for ind in tqdm(matchesdf.index):
        events = get_matchFree(matchesdf[matchesdf.index == ind]['match_id'].values[0],
                               env=env)
        events.loc[:, 'competition_id'] = matchesdf[matchesdf.index == ind]['competition.competition_id'].values[0]
        events.loc[:, 'season_id'] = matchesdf[matchesdf.index == ind]['season.season_id'].values[0]
        res.append(events)
    df = pd.concat(res, sort=True)
    return df

# Function to retrieve lineup from a match.
# Returns events (DataFrame): DataFrame with all events.
def get_lineupsFree(match_id, env='local'):

    events_url = config.data_dir + f"lineups/{match_id}.json"
    with open(events_url, encoding='utf-8') as json_file:
        raw_events_api = json.load(json_file)
    events = pd.DataFrame(json_normalize(
        raw_events_api, 'lineup', ['team_id', 'team_name']))
    
    events.loc[:, 'match_id'] = match_id
    return events

# Function to create DataFrame with events from match.
# Returns: df (DataFrame): DataFrame with all events from all matches.
def StatsBombFreelineups(matchesdf, env='local'):
    res = []
    for ind in matchesdf.index:
        events = get_lineupsFree(matchesdf[matchesdf.index == ind]['match_id'].values[0],
                                 env=env)
        events.loc[:, 'competition_id'] = matchesdf[matchesdf.index == ind
                                                    ]['competition.competition_id'].values[0]
        events.loc[:, 'season_id'] = matchesdf[matchesdf.index == ind
                                               ]['season.season_id'].values[0]
        res.append(events)
    df = pd.concat(res, sort=True)
    return df

