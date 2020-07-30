import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
import matplotlib.colors
import matplotlib.patches as patches
import matplotlib.cm as cm
from data_functions import compute_defensive_actions, minutes_played, draw_field

messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'df_messi.csv'

# This file should be used alongside heatmap.py. Contrast the strength of the defence with how well a player (probs Messi) played.

# Use the match id and compare/contrast defence to how well Messi did in the game. Logcally, if the defence was good the impact will be less.

# Defensive map needs the data for the entire season for a team then compare the game with highest/lowest xp to the average.

def calculate_defensive_actions_season(season_id = 21, highest = False):

    """
        Function which will get the defensive stats for a particular season accross all of the league. Then create a map which will show if a 
        particular game has more or less defensive pressure than the seasons mean.

        Args:
            season_id (int): season of which to get the defensive stats for.
            highest (bool): Whtether to use the highest or lowest xg of Messi to compare against.
        
        Returns:

    """
    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # A list of all the match ids of a given season.
    all_match_ids = df_messi[df_messi['season_id'] == season_id]['match_id'].values

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
        match_id = get_highest_xG(df_messi, all_match_ids)
    else:
        match_id = get_lowest_xG(df_messi, all_match_ids)
    
    df_messi[df_messi['match_id'] == match_id][['home_score', 'away_score', 'home_team.home_team_name', 'away_team.away_team_name']]

    #--
    
    fig, ax = plt.subplots()
    fig.set_size_inches(14, 8)
    draw_field(ax)

    minima = -20
    maxima = 20

    norm = matplotlib.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap= 'coolwarm')

    plt.colorbar(mapper, shrink=0.7, label='Distance from average')

    # Visualization of defensive actions of Espanyol
    for index, row in season_dataframe[season_dataframe['match_id'] == match_id].iterrows():
        mean_def = season_dataframe_mean[(season_dataframe_mean['x_min'] == row['x_min']) & (season_dataframe_mean['x_max'] == row['x_max']) &
                (season_dataframe_mean['y_min'] == row['y_min']) & (season_dataframe_mean['y_max'] == row['y_max']) ]['def_opponent'].values[0]

        # Create a Rectangle patch
        rect = patches.Rectangle((row['x_min'], row['y_min']), row['x_max'] - row['x_min'], row['y_max'] - row['y_min'], linewidth=1,
            edgecolor='none', facecolor=mapper.to_rgba(row['def_opponent']-mean_def),)

        # Add the patch to the Axes
        ax.add_patch(rect)

    ax.add_patch(patches.Ellipse((40, 10), width=70, height=24, edgecolor='red', fill=False, linewidth=4 ))

    fig.savefig('espanyol_defensive_map.png')




# Return the match id with the lowest xG
def get_lowest_xG(df_messi, all_match_ids):
    xg_0910 = df_messi[(df_messi['match_id'].isin(all_match_ids)) & (df_messi['player.name'] == messi_name) ].groupby('match_id')['shot.statsbomb_xg'].sum()

    xg_0910_per90 = pd.Series(data=[90 * xg_0910[x] / minutes_played(df_messi, x, messi_name, 'Barcelona' ) for x in xg_0910.index],index=xg_0910.index)

    index_min_xg = xg_0910_per90.argmin()

    # The game with the lowest xG
    return xg_0910_per90.index[index_min_xg]

# Return the match id with the highest xG
def get_highest_xG(df_messi, all_match_ids):
    xg_0910 = df_messi[(df_messi['match_id'].isin(all_match_ids)) & (df_messi['player.name'] == messi_name) ].groupby('match_id')['shot.statsbomb_xg'].sum()

    xg_0910_per90 = pd.Series(data=[90 * xg_0910[x] / minutes_played(df_messi, x, messi_name, 'Barcelona' ) for x in xg_0910.index],index=xg_0910.index)

    index_max_xg = xg_0910_per90.argmax()

    # The game with the highest xG
    return xg_0910_per90.index[index_max_xg]


if __name__ == '__main__':
    # season_ids = [4, 1, 2, 27, 26, 25, 24, 23, 22, 21, 41, 40, 39, 38, 37]
    calculate_defensive_actions_season()