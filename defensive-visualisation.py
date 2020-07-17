import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm

messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'messi_events.csv'

# This file should be used alongside heatmap.py. Contrast the strength of the defence with how well a player (probs Messi) played.

# Use the match id and compare/contrast defence to how well Messi did in the game. Logcally, if the defence was good the impact will be less.

# Defensive map needs the data for the entire season for a team then compare the game with highest/lowest xp to the average.

def calculate_defensive_actions_season(season_id = 21):
    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # A list of all the match ids of a given season.
    all_match_ids = df_messi[df_messi['season.season_id'] == season_id]['match_id'].values

    x_min_cut = range(0, 120, 20)
    x_max_cut = range(20, 121, 20)
    y_min_cut = range(0, 80, 16)
    y_max_cut = range(16, 81, 16)

    # Empty dataframe creation for results
    season_dataframe = pd.DataFrame(columns=['match_id','x_min', 'x_max', 'y_min', 'y_max', 'def_barca', 'def_opponent'])

    # Calculation of defensive actions for all matches from 2009/2010
    for match_id in tqdm(all_match_ids):
        def_actions = []
        for x_min, x_max in zip(x_min_cut, x_max_cut):
            for y_min, y_max in zip(y_min_cut, y_max_cut):
                def_window = compute_def_actions(df_messi, match_id, x_min, x_max, y_min, y_max)
                opponent = [list(def_window.keys())[0] if list(def_window.keys())[0] != 'Barcelona' else list(def_window.keys())[1]][0]
                def_actions.append([match_id, x_min, x_max, y_min, y_max, def_window['Barcelona'], def_window[opponent]])

        temp_df = pd.DataFrame(data=def_actions,
                           columns=['match_id','x_min', 'x_max',
                                    'y_min', 'y_max',
                                    'def_barca', 'def_opponent'])

        def_actions_0910 = def_actions_0910.append(temp_df, ignore_index=True)






if __name__ == '__main__':
    # season_ids = [4, 1, 2, 27, 26, 25, 24, 23, 22, 21, 41, 40, 39, 38, 37]
    calculate_defensive_actions_season()