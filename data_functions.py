# Stats from StatsBomb free datasets. Gets from github

import pandas as pd
from pandas import json_normalize
import json
import requests
from tqdm.auto import tqdm

import matplotlib.pyplot as plt
from matplotlib.patches import Arc

import numpy as np
from scipy.ndimage.filters import gaussian_filter

from ast import literal_eval

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
def StatsBombFreeEvents(matchesdataframe):
    """Function to create DataFrame with events from match.

        Args:
            matchesdataframe (DataFrame): dataframe of matches. Must have columns 'match_id', 'competition_id', and 'season_id'.
    
        Returns:
            dataframe (DataFrame): DataFrame with all events from all matches.

    """
    res = []
    for ind in tqdm(matchesdataframe.index):
        events = get_match_free(matchesdataframe[matchesdataframe.index == ind]['match_id'].values[0])
        events.loc[:, 'competition_id'] = matchesdataframe[matchesdataframe.index == ind]['competition.competition_id'].values[0]
        events.loc[:, 'season_id'] = matchesdataframe[matchesdataframe.index == ind]['season.season_id'].values[0]
        res.append(events)
    dataframe = pd.concat(res, sort=True)
    return dataframe


def get_lineups(match_id):
    """ Function which gets the lineup from a given match id.

    Args:
        match_id (int) : id of the game

    Returns:
        events (DataFrame): DataFrame with all events.

    """

    events_url = stats_bomb_url + f"lineups/{match_id}.json"
    raw_events_api = requests.get(url=events_url)
    raw_events_api.encoding = 'utf-8'
    events = pd.DataFrame(json_normalize(raw_events_api.json(), 'lineup', ['team_id', 'team_name']))
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


def minutes_played(dataframe, match_id, player_name, team_name):
    """
        Function that gets the minutes played (in a game) for a player.
        Checks if player was a starter or a substitute. 
        Checks if the player recieved a card which reduced playing time.

        Args:
            dataframe (DataFrame): dataframe of events of games (created from Stastbomb open data).
            match_id (int): id of the game.
            player_name (String): player name to use
            team_name (String): Name of the team to use.

        Returns:
            minutes_played (float) : Number of minutes played by a given player.

    """
    # Create a col for time in the dataframe.
    dataframe['time'] = (dataframe['minute'] * 60 + dataframe['second'] ) / 60

    # Get the lineup for the match_id
    lineup = literal_eval(dataframe[(dataframe['match_id'] == match_id) &(dataframe['team.name'] == team_name) 
        & (dataframe['type.name'] == 'Starting XI')]['tactics.lineup'].values[0])

    starting_lineup = [x['player']['name'] for x in lineup]
    
    first_half_duration = dataframe[(dataframe['match_id'] == match_id) & (dataframe['period'] == 1)]['time'].max()

    second_half_duration = dataframe[(dataframe['match_id'] == match_id) & (dataframe['period'] == 2)]['time'].max() - 45

    # Player started the game
    if player_name in starting_lineup:

        # If the player started the game. Give them the full duration of the game. Take into account substitions later.
        minutes_played = first_half_duration + second_half_duration

    else:
        # Check to see if the player entered the game through a substitution.
        subbed_in = dataframe[(dataframe['match_id'] == match_id) &
            (dataframe['team.name'] == team_name) &(dataframe['type.name'] == 'Substitution') &
            (dataframe['substitution.replacement.name'] == player_name)][['time', 'period']]

        # Player was subbed into the game. Calculate the time played.
        if not subbed_in['time'].empty:
            minutes_played = int(subbed_in['period'] == 1)*(first_half_duration - subbed_in['time'].values[0] + second_half_duration)
            + int(subbed_in['period'] == 2)*(second_half_duration + 45 - subbed_in['time'].values[0])

        else:
            # Player didn't enter the game so minutes played is 0.
            minutes_played = 0
        
    # Check if the player (checking starters here) was substituted during the game.
    was_subbed = dataframe[(dataframe['match_id'] == match_id) & (dataframe['team.name'] == team_name) & 
        (dataframe['player.name'] == player_name) & (dataframe['type.name'] == 'Substitution')][['time', 'period']]
    
    # The player was subbed. (Time isn't empty). Reduce the minutes played by the player.
    if not was_subbed['time'].empty:
        minutes_played = minutes_played - int(was_subbed['period'].values == 1)*(second_half_duration + first_half_duration - was_subbed['time'].values[0]
            ) + int(was_subbed['period'].values == 2)*(second_half_duration + 45 - was_subbed['time'].values[0])
    

    # Check if a player recieved a red/yellow card. 
    was_carded = dataframe[(dataframe['match_id'] == match_id) & (dataframe['team.name'] == team_name) &(dataframe['player.name'] == player_name) 
        & ((dataframe['bad_behaviour.card.name' ].isin(['Red Card', 'Second Yellow'])) 
        | (dataframe['foul_committed.card.name'].isin(['Red Card', 'Second Yellow'])))][['time', 'period']]

    # Player recieved a card, so we reduce the minutes_played in the game.
    if not was_carded['time'].empty:
        minutes_played = minutes_played - int(was_carded['period'].values == 1 )*(second_half_duration + first_half_duration - was_carded['time'].values[0]
            ) + int(was_carded['period'].values == 2)*(second_half_duration + 45 - was_carded['time'].values[0])
    
    # Could check for minutes played > 0 incase of divide by 0 errors.
    return minutes_played


def compute_defensive_actions(dataframe, match_id, x_min=0.0, x_max=120.0, y_min=0.0, y_max=80.0):
    """
        Function to calculate the defensive actions for each time in a game. 

        Args:
            dataframe (DataFrame): dataframe with Statsbomb event data.
            match_id (int): match id of the game we want to calculate the metric on.
            x_min (float): min on the location_x. 
            x_max (float): max on the location_x. 
            y_min (float): min on the location_y. 
            y_max (float): max on the location_y. 

        Returns:
            res (dict): number of defensive actions for each team in a dict with keys equal to team names.
    """

    # Get all unique team names
    all_teams = dataframe[dataframe['match_id'] == match_id]['team.name'].unique()

    # Filter dataframe for the specific match_id and area of the pitch
    dataframe_match = dataframe[(dataframe['match_id'] == match_id) & (dataframe['location_x'] >= x_min) & (dataframe['location_x'] <= x_max) &
        (dataframe['location_y'] >= y_min) & (dataframe['location_y'] <= y_max)].reset_index(drop=True)

    defensive_events = ['Block', 'Clearance', 'Foul Commited', 'Interception', 'Duel', 'Pressure', 'Shield']

    res = {}

    for team in all_teams:
        # Team number of defensive actions
        defensive_actions = len(dataframe_match[(dataframe_match['team.name'] == team) & (dataframe_match['type.name'].isin(defensive_events))])

        # Adding blocked shot (shot from opposition team) in the count
        defensive_actions += len(dataframe_match[(dataframe_match['team.name'] != team) & (dataframe_match['type.name'] == 'Shot') & (dataframe_match['shot.outcome.name'] == 'Blocked')])

        # Adding "defensive" pass: Pass with type Interception and Recovery
        defensive_actions += len(dataframe_match[(dataframe_match['team.name'] == team) & (dataframe_match['type.name'] == 'Pass') & 
            (dataframe_match['pass.type.name'].isin(['Interception', 'Recovery']))])

        defensive_actions += len(dataframe_match[(dataframe_match['team.name'] != team) &(dataframe_match['type.name'] == 'Dispossessed')])
        
        res[team] = defensive_actions

    return res




# Next set of functions will be to do with drawing the football pitch and other things like heatmaps, passmaps etc...


def draw_field(ax, heatmap=False ,field_colour= "#195905", line_colour= "#000000"):

    """
        Function to draw a football field with the dimensions from statsbomb docs (See page 22 opendata/docs/OpenDataEvents.pdataframe)
    
        Args:
            heatmap (Boolean) : Won't add background rectangles if heatmap = True
            field_colour (Color/Hex) : Colour for the field.
            line_colour (Color/Hex) : Colour of the lines on the field.
        
        Retuns:
            ax (axes): Matplotlib axes.

    """

    # Call these from the original place you want to create a pitch. Pass ax to the function.
    # fig, ax = plt.subplots()
    # fig.set_size_inches(10, 6.5)

    x_min = 0
    x_max = 120
    y_min = 0
    y_max = 80

    linewidth = 2

    # Outline of the Field.
    plt.plot([x_min, y_min], [x_min, y_max], color=line_colour, linewidth=linewidth)
    plt.plot([x_min, x_max], [y_max, y_max], color=line_colour, linewidth=linewidth)
    plt.plot([x_max, x_max], [y_max, y_min], color=line_colour, linewidth=linewidth)
    plt.plot([x_max, y_min], [x_min, y_min], color=line_colour, linewidth=linewidth)

    # Centre line.
    plt.plot([x_max/2, x_max/2], [x_min, y_max], color=line_colour, linewidth=linewidth)

    # Left penalty area.
    plt.plot([18, 18], [62, 18], color=line_colour, linewidth=linewidth)
    plt.plot([0, 18], [62, 62], color=line_colour, linewidth=linewidth)
    plt.plot([0, 18], [18, 18], color=line_colour, linewidth=linewidth)

    # Right Penalty Area
    plt.plot([120, 102], [62, 62], color=line_colour, linewidth=linewidth)
    plt.plot([120, 102], [18, 18], color=line_colour, linewidth=linewidth)
    plt.plot([102, 102], [18, 62], color=line_colour, linewidth=linewidth)

    # Left 6-yard Box
    plt.plot([6, 6], [30, 50], color=line_colour, linewidth=linewidth)
    plt.plot([0, 6], [50, 50], color=line_colour, linewidth=linewidth)
    plt.plot([0, 6], [30, 30], color=line_colour, linewidth=linewidth)

    # Right 6-yard Box
    plt.plot([120, 114], [30, 30], color=line_colour, linewidth=linewidth)
    plt.plot([114, 114], [50, 30], color=line_colour, linewidth=linewidth)
    plt.plot([120, 114], [50, 50], color=line_colour, linewidth=linewidth)  


    # Adding colour Rectangles in boxes
    rectangle_1 = plt.Rectangle((87.5,20), 16,30,ls='-',color=field_colour, zorder=1,alpha=1)
    rectangle_2 = plt.Rectangle((0, 20), 16.5,30,ls='-',color=field_colour, zorder=1,alpha=1)

    # Adding colour Pitch rectangle
    rectangle_3 = plt.Rectangle((0, 0), 120, 80,ls='-',color=field_colour, zorder=1,alpha=1)

    # Prepare Circles
    centre_circle = plt.Circle((x_max/2, y_max/2), 10, color=line_colour, fill=False, linewidth=linewidth)
    centre_spot = plt.Circle((x_max/2, y_max/2), 0.9, color=line_colour, linewidth=linewidth)

    left_penalty_spot = plt.Circle((12, 40), 0.71, color=line_colour)
    right_penalty_spot = plt.Circle((108, 40), 0.71, color=line_colour)

    # Prepare Arcs
    left_arc = Arc((13, 40), height=16.2, width=16.2, angle=0, theta1=310, theta2=50, color=line_colour, linewidth=linewidth)
    right_arc = Arc((107, 40), height=16.2, width=16.2, angle=0, theta1=130, theta2=230, color=line_colour, linewidth=linewidth)


    # If we are drawing a pitch for a heatmap we DON'T want to add the 'background' rectangles.
    if not heatmap:
        ax.add_artist(rectangle_1)
        ax.add_artist(rectangle_2)
        ax.add_artist(rectangle_3)

    # Draw Circles
    ax.add_artist(centre_circle)
    ax.add_artist(centre_spot)
    ax.add_artist(left_penalty_spot)
    ax.add_artist(right_penalty_spot)

    # Draw Arcs
    ax.add_artist(left_arc)
    ax.add_artist(right_arc)

    plt.xlim([-5, 125])
    plt.ylim([-5, 85])

    plt.axis('off')

    # invert the axis so iut matches the sheet from statsbomb docs
    ax.invert_yaxis()

    return ax


# Followed this guide https://numpy.org/doc/stable/reference/generated/numpy.histogram2d.html
def create_heatmap(x, y, s, bins=1000):
    """
        Function to return a 'Heatmap' Place this on top of a football field.

    """
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [0, 120, 0, 80]
    return heatmap.T, extent


