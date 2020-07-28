from data_functions import compute_defensive_actions, minutes_played, draw_field
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.patches as patches
import matplotlib.cm as cm


messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'messi_events.csv'

def calculate_pass_map(season_id = 21, highest = False):
    """
    Must have the columns 'end_location_x and end_location_y.


    """

    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # Get all of the match ID's of games which feature Messi from the season with ID 21.
    # Stored as a numpy array. To remove dupes in the data use np.unique(dataset)
    match_id = df_messi[df_messi['season_id'] == season_id]['match_id'].values

    # Games with lowest xG
    lowest_xG_games = df_messi[(df_messi['match_id'].isin(match_id)) & (df_messi['player.name'] == messi_name)].groupby('match_id')['shot.statsbomb_xg'].sum()

    # Lowest xG per 90 game.
    lowest_xG_per_90_game = pd.Series(data=[90 * lowest_xG_games[x] / minutes_played(df_messi, x, messi_name, 'Barcelona') for x in lowest_xG_games.index], index=lowest_xG_games.index)

    index_min_xg = lowest_xG_per_90_game.argmin()

    # The match id of the game with the lowest expected goals.
    match_id_lowest_xG_game = lowest_xG_per_90_game.index[index_min_xg]

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    
    draw_field(ax, heatmap=True)

    for index, row in df_messi[(df_messi['match_id'] == match_id_lowest_xG_game) & (df_messi['player.name'] == messi_name) & (df_messi['type.name'] == 'Pass')].iterrows():
        if row['pass.outcome.name'] == 'Incomplete':
            if row['under_pressure'] == True:
                color = "salmon"
            else:
                color = "firebrick"
        else:
            if row['under_pressure'] == True:
                color = 'lightgreen'
            else:
                color = 'seagreen'
        
        print(row['end_location_x'], row['end_location_y'])
        ax.arrow(row['location_x'], row['location_y'], row['end_location_x'] - row['location_x'], row['end_location_y'] - row['location_y'], 
            color=color, linewidth=1.5, head_width=1.5, length_includes_head=True)



    greenPatch_up = matplotlib.patches.Rectangle((0, 0), 0, 0, color = 'lightgreen')
    redPatch_up = matplotlib.patches.Rectangle((0, 0), 0, 0, color = 'salmon')

    greenPatch = matplotlib.patches.Rectangle((0, 0), 0, 0, color = 'seagreen')
    redPatch = matplotlib.patches.Rectangle((0, 0), 0, 0, color = 'firebrick')

    leg = ax.legend([greenPatch_up, greenPatch, redPatch_up, redPatch],
                ['Complete - under pressure', 'Complete - no pressure',
                 'Incomplete - under pressure', 'Incomplete - no pressure'],
                loc='upper right',
                bbox_to_anchor = (1, 1.1),
                fontsize=12,
                ncol=2)

    plt.plot([80, 80], [0, 80],
         color='grey',
         linewidth=2,
         linestyle='--'
         )

    plt.text(80, 83, "<---------------   Final Third    -------------->",
         {'color': 'grey', 'fontsize': 12})


    ax.set_title("Messi pass map",
             loc='left')

    fig.savefig('messi_pass_map.png')
        

if __name__ == '__main__':
    calculate_pass_map()