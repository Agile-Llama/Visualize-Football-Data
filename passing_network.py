
from ast import literal_eval
from data_functions import minutes_played, get_lineups, draw_field
import pandas as pd
from pandas import json_normalize
import matplotlib.pyplot as plt
import json
import requests

# Github root url for statsbomb data.
stats_bomb_url = 'https://raw.githubusercontent.com/statsbomb/open-data/master/data/'

# Folder in which to save lineup json file.
data_folder = '/Users/agilellama/Desktop/Free-Kick-Visualization/Data/Lineups/'

messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'df_messi.csv'

def draw_passing_network(ax, dataframe, match_id, team_name, min_time=0, max_time=None):
    """
        Function to draw a passing network of a particular match. 
        Inspired by https://github.com/Friends-of-Tracking-Data-FoTD/passing-networks-in-python
            (under visualization/passing_network.py)
        
        Args:
            ax: Matplotlib's axis object, expected that the pitch has already been plotted.
            dataframe (dataframe): A dataframe with the events of the game.
            match_id (int): The id of the match in which the function will draw.
            team_name (string): The name of the team.
            min_time (opt, float): The minimum time to start from.
            max_time (opt, float): Defaults to none. The max time by default is while both sides of the first XI are on.
        
        Returns:
            ax (axes): Matplotlib axes.
    """

    # Whoever is in the starting lineup of the team will be on the passing network.
    starting_lineup = literal_eval(dataframe[(dataframe['match_id'] == match_id) &
                             (dataframe['type.name'] == 'Starting XI') &
                             (dataframe['team.name'] == team_name)
                             ]['tactics.lineup'].values[0])
    
    if max_time is None:
        # Get number of played minutes for this game for each player
        min_played = []
        for player in starting_lineup:
            min_played.append(minutes_played(dataframe, match_id,player['player']['name'],team_name))

        # The max amount of time is while all the starting lineup is on the field.
        # This is the number in which someone is removed from the game.
        max_time = min(min_played)
    
    # Filter passes for passes before first sub or first red card
    # Passes with 'NaN' mean complete.
    dataframe_passes = dataframe[(dataframe['match_id'] == match_id) & (dataframe['type.name'] == "Pass") & (dataframe['pass.outcome.name'].isna()) &
        (dataframe['team.name'] == team_name) & (dataframe['time'] >= min_time) & (dataframe['time'] <= max_time)].copy()
    
    # Get the lineups and save the json file into the 'Data' folder. Used to get the nicknames of the players.
    lineup_df = get_lineups(match_id)
    # lineup_df.to_json('%s%s.json' % (data_folder, match_id), orient='columns')

    # with open('/Users/agilellama/Desktop/Free-Kick-Visualization/Data/Lineups/15956.json', encoding='utf-8') as json_file:
    #     lineup_file = json.load(json_file)

    # names_nickames = {player["player_name"]: player["player_nickname"] for team in lineup_file for player in team['lineup'].values()}

    # Look at inspiration github code to see if more obvious

    

# Loads the highest/lowest xG game. Then calls the draw_passing_network function.
def start(season_id, highest=False):
    df_messi = pd.read_csv('df_messi.csv', index_col=0, low_memory=False)
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
    
    # The match id of the game with the lowest/highest xG.
    match_id = xG_per_90_game.index[index_min_xg]

    fig = plt.figure()
    ax = fig.add_subplot()

    fig.set_size_inches(12, 8)
    draw_field(ax)

    draw_passing_network(ax, df_messi, match_id, 'Barcelona')

if __name__ == '__main__':
    #season_ids = [4, 1, 2, 27, 26, 25, 24, 23, 22, 21, 41, 40, 39, 38, 37]
    #for i in tqdm(season_ids):
    #    start(i)
    start(4)




    

