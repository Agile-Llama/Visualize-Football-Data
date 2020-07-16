import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from data_functions import FreeCompetitions, FreeMatches, create_heatmap, draw_field, minutes_played

import os

# Full name
messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'messi_events.csv'



def lowest_xg_game():
    """
        Function that gets the lowest Expected Goals game in Lionel Messi's career.
        A heatmap is created and saved to the current working directory as 'messi_heatmap_lowest_xG.png'

        Note, the game should be 2009/10 against Espanyol with the match id of 69213.
    """
    
    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # Get all of the match ID's of games which feature Messi.
    # Stored as a numpy array. To remove dupes in the data use np.unique(dataset)
    match_id = df_messi[df_messi['season_id'] == 21]['match_id'].values

    # Game with lowest xG
    lowest_xG_games = df_messi[(df_messi['match_id'].isin(match_id)) & (df_messi['player.name'] == messi_name)].groupby('match_id')['shot.statsbomb_xg'].sum()

    # Lowest xG per 90 game.
    lowest_xG_per_90_game = pd.Series(data=[90 * lowest_xG_games[x] / minutes_played(df_messi, x, messi_name, 'Barcelona') for x in lowest_xG_games.index], index=lowest_xG_games.index)

    index_min_xg = lowest_xG_per_90_game.argmin()

    # The match id of the game with the lowest expected goals.
    match_id_lowest_xG_game = lowest_xG_per_90_game.index[index_min_xg]

    # Messi heatmap to compare to.
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    draw_field(ax, heatmap=True)

    data_from_lowest_xg_game = df_messi[(df_messi['match_id'] == match_id_lowest_xG_game) & (df_messi['player.name'] == messi_name) & (~df_messi['location_x'].isnull()) & (~df_messi['location_y'].isnull())]

    sigma = 50

    img, extent = create_heatmap(120 - data_from_lowest_xg_game['location_x'], 80 - data_from_lowest_xg_game['location_y'], sigma)
    ax.imshow(img, extent=extent, origin='lower', cmap=cm.jet)
    ax.set_title("Heatmap of Lionel Messi", loc='left')

    ax.annotate(f"Espanyol - Barcelona (2009/2010)", xy=(90, -5))

    ax.annotate("Direction of play for Barcelona", xy=(5, 83), xytext=(60, 84), arrowprops=dict(arrowstyle="->", edgecolor='k', linewidth=1.5), color='k')

    fig.savefig('messi_heatmap_lowest_xG.png')


if __name__ == '__main__':
    lowest_xg_game()

