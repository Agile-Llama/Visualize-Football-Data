import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

from data_functions import compute_defensive_actions, minutes_played

messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'messi_events.csv'

# This file should be used alongside heatmap.py. Contrast the strength of the defence with how well a player (probs Messi) played.

# Use the match id and compare/contrast defence to how well Messi did in the game. Logcally, if the defence was good the impact will be less.

# Defensive map needs the data for the entire season for a team then compare the game with highest/lowest xp to the average.

def calculate_defensive_actions_season(season_id = 21, highest = True):
    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # A list of all the match ids of a given season.
    all_match_ids = df_messi[df_messi['season.season_id'] == season_id]['match_id'].values

    x_min_cut = range(0, 120, 20)
    x_max_cut = range(20, 121, 20)
    y_min_cut = range(0, 80, 16)
    y_max_cut = range(16, 81, 16)

    # Empty dataframe creation for results
    season_dataframe = pd.DataFrame(columns=['match_id','x_min', 'x_max', 'y_min', 'y_max', 'def_barca', 'def_opponent'])

    # Calculation of defensive actions for all matches from a given season id
    for match_id in tqdm(all_match_ids):
        def_actions = []
        for x_min, x_max in zip(x_min_cut, x_max_cut):
            for y_min, y_max in zip(y_min_cut, y_max_cut):
                defensive_window = compute_defensive_actions(df_messi, match_id, x_min, x_max, y_min, y_max)
                opponent = [list(defensive_window.keys())[0] if list(defensive_window.keys())[0] != 'Barcelona' else list(defensive_window.keys())[1]][0]
                def_actions.append([match_id, x_min, x_max, y_min, y_max, defensive_window['Barcelona'], defensive_window[opponent]])

        temp_df = pd.DataFrame(data=def_actions,columns=['match_id', 'x_min', 'x_max', 'y_min', 'y_max', 'def_barca', 'def_opponent'])
        season_dataframe = season_dataframe.append(temp_df, ignore_index=True)

    # Compute the average number of defensive actions per pitch zone
    # Average value for Barca on one side and for its opponents on the other side
    defensive_means = []
    for x_min, x_max in zip(x_min_cut, x_max_cut):
        for y_min, y_max in zip(y_min_cut, y_max_cut):
            means = season_dataframe[(season_dataframe['x_min'] == x_min) &(season_dataframe['x_max'] == x_max) &
                        (season_dataframe['y_min'] == y_min) & (season_dataframe['y_max'] == y_max)][['def_barca', 'def_opponent']].mean()
        
            defensive_means.append([x_min, x_max, y_min, y_max, means['def_barca'], means['def_opponent']])
    
    season_dataframe_mean = pd.DataFrame(data=defensive_means, columns=['x_min', 'x_max', 'y_min', 'y_max', 'def_barca', 'def_opponent'])

    # Expected goal per 90 during a given season.
    average_expected_goals_season = 90 * df_messi[(df_messi['season_id'] == season_id) & (df_messi['player.name'] == messi_name)]['shot.statsbomb_xg'].sum() / minutes_played(df_messi, season_id, messi_name,'Barcelona')

    # Can get either the highest or lowest expected goal match id.
    if highest:
        match_id = get_highest_xp()
    else:
        match_id = get_lowest_xg()


# Return the match id with the lowest xG
def get_lowest_xg(df_messi, all_match_ids):
    xg_0910 = df_messi[(df_messi['match_id'].isin(all_match_ids)) & (df_messi['player.name'] == messi_name) ].groupby('match_id')['shot.statsbomb_xg'].sum()

    xg_0910_per90 = pd.Series(data=[90 * xg_0910[x] / minutes_played(df_messi, x, messi_name, 'Barcelona' ) for x in xg_0910.index],index=xg_0910.index)

    index_min_xg = xg_0910_per90.argmin()

    # The game with the lowest xG
    return xg_0910_per90.index[index_min_xg]

# Return the match id with the highest xG
def get_highest_xg(df_messi, all_match_ids):
    xg_0910 = df_messi[(df_messi['match_id'].isin(all_match_ids)) & (df_messi['player.name'] == messi_name) ].groupby('match_id')['shot.statsbomb_xg'].sum()

    xg_0910_per90 = pd.Series(data=[90 * xg_0910[x] / minutes_played(df_messi, x, messi_name, 'Barcelona' ) for x in xg_0910.index],index=xg_0910.index)

    index_max_xg = xg_0910_per90.argmax()

    # The game with the highest xG
    return xg_0910_per90.index[index_max_xg]





if __name__ == '__main__':
    # season_ids = [4, 1, 2, 27, 26, 25, 24, 23, 22, 21, 41, 40, 39, 38, 37]
    calculate_defensive_actions_season()