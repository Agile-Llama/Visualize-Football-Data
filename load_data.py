# Stats from StatsBomb free datasets
import pandas as pd
from data_functions import FreeMatches, FreeCompetitions, StatsBombFreeEvents

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

free_comp = FreeCompetitions()

def all_la_liga_data():
    """
        Function to get all the events from all laliga seasons in free competitions.
        Writes these events to a csv file called 'lalaiga_events.csv'
    """
    laliga_matches = FreeMatches(free_comp[free_comp.competition_id == 11].reset_index())

    # Running this will take about 8-10mins
    laliga_events = StatsBombFreeEvents(laliga_matches)

    # Writing to csv file takes about 15mins (Doing all the operations above)
    laliga_events.to_csv('laliga_events.csv')


def all_messi_events():
    """
        Function to get all the events which feature the player Lionel Andrés Messi Cuccittini
        Writes these events to a csv file called 'messi_events.csv'
    """
    laliga_matches = FreeMatches(free_comp[free_comp.competition_id == 11].reset_index())

    # Running this will take about 8-10mins
    laliga_events = StatsBombFreeEvents(laliga_matches)

    # Get all the events of a specific player.
    final = laliga_events[(laliga_events['player.name'] == 'Lionel Andrés Messi Cuccittini')]

    final.to_csv('messi_events.csv')
        
    