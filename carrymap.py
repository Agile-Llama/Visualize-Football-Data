from data_functions import compute_defensive_actions, minutes_played, draw_field
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches as patches
import matplotlib.cm as cm
from tqdm.auto import tqdm

messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'df_messi.csv'


def calculate_carry_map(season_id = 21, highest = False):
    """
        Must have the columns 'end_location_x and end_location_y.
        Function which creates a carrymap for Lionel Messi for the lowest or highest expected goal game in a given season. 

        Args:
            season_id(int): Season in which to get the lowest Expected Goal game.
            highest(bool): If True want the game with the game with the HIGHEST Expected Goals.

    """ 

    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # Get all of the match ID's of games which feature Messi from the season with ID 21.
    # Stored as a numpy array. To remove dupes in the data use np.unique(dataset)
    match_id = df_messi[df_messi['season_id'] == season_id]['match_id'].values

    # All games (group by match_id)
    all_games = df_messi[(df_messi['match_id'].isin(match_id)) & (df_messi['player.name'] == messi_name)].groupby('match_id')['shot.statsbomb_xg'].sum()

    # calculate the expected goals of each game. 
    xG_per_90_game = pd.Series(data=[90 * all_games[x] / minutes_played(df_messi, x, messi_name, 'Barcelona') for x in all_games.index], index=all_games.index)

    # This decides if we are getting the lowest or highest xG game.
    if highest:
        index_min_xg = xG_per_90_game.argmax()
    else:
        index_min_xg = xG_per_90_game.argmin()
    
    match_id = xG_per_90_game.index[index_min_xg]

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    
    draw_field(ax, heatmap=False)

    for index, row in df_messi[(df_messi['match_id'] == match_id) & (df_messi['player.name'] == messi_name) & (df_messi['type.name'] == 'Carry')].iterrows():

        if row['under_pressure'] == True:
            color = "royalblue"
        else:
            color = "cyan"

        # Draw the arrow on the field. Could include pressure dribbles. For now not. 
        # Note zorder is set to 2. This is to put it on top of the green field and the lines.
        ax.arrow(row['location_x'], row['location_y'], row['end_location_x'] - row['location_x'], row['end_location_y'] - row['location_y'], 
            color=color, linewidth=1.5, head_width=1.5, length_includes_head=True, zorder=2)
    
    green_patch_up = matplotlib.patches.Rectangle((0, 0), 0, 0, color = 'royalblue')
    green_patch = matplotlib.patches.Rectangle((0, 0), 0, 0, color = 'cyan')

    # Add the legend for the pitch. There are 4 colours which all represent a specific type of pass.
    leg = ax.legend([green_patch_up, green_patch], ['Dribble - Pressure ','Dribble - No Pressure'], loc='upper right', bbox_to_anchor = (1, 1.1), fontsize=12, ncol=2)

    plt.plot([80, 80], [0, 80], color='grey', linewidth=2, linestyle='--' )

    # Annotate on the pitch the final third. Passes into the final third generally have lower success rate.
    plt.text(80, 83, "<---------------   Final Third    -------------->", {'color': 'grey', 'fontsize': 12})

    ax.set_title("Carry map of Lionel Messi", loc='left')

    ax.annotate(f"Match Id: %d Season Id: %d" % (match_id, season_id), xy=(90, -2))

    # ax.annotate("Direction of play for Barcelona", xy=(5, 83), xytext=(60, 84), arrowprops=dict(arrowstyle="->", edgecolor='k', linewidth=1.5), color='k')

    if highest:
        fig.savefig('Carrymaps/Highest_xG/S%d_Messi_Carrymap_Highest_xG.png' % (season_id))
    else:
        fig.savefig('Carrymaps/Lowest_xG/S%d_Messi_Carrymap_Lowest_xG.png' % (season_id))
    

if __name__ == '__main__':
    season_ids = [4, 1, 2, 27, 26, 25, 24, 23, 22, 21, 41, 40, 39, 38, 37]
    for i in tqdm(season_ids):
       calculate_carry_map(i, highest=True)
       calculate_carry_map(i, highest=False)

    # print('Nothing called..')