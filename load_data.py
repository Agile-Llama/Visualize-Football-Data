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

    # Below explained. Statsbomb data for the below stats come as a pair ie ([55, 65]) this breaks that one up into 2 for easier reading in future.

    # Create column for end_location x and y. For PASSING.
    final.loc[final['type.name'] == 'Pass','end_location_x'] = [x[0] for x in final[final['type.name'] == 'Pass']['pass.end_location']]
    final.loc[final['type.name'] == 'Pass', 'end_location_y'] = [x[1] for x in final[final['type.name'] == 'Pass']['pass.end_location']]

    # Create column for end_location x and y. For CARRY.
    final.loc[final['type.name'] == 'Carry', 'end_location_x'] = [x[0] for x in final[final['type.name'] == 'Carry' ]['carry.end_location']]
    final.loc[final['type.name'] == 'Carry', 'end_location_y'] = [x[1] for x in final[final['type.name'] == 'Carry']['carry.end_location']]

    # Create column for end_location x and y. For SHOT.
    final.loc[final['type.name'] == 'Shot', 'end_location_x'] = [x[0] for x in final[final['type.name'] == 'Shot' ]['shot.end_location']]
    final.loc[final['type.name'] == 'Shot', 'end_location_y'] = [x[1] for x in final[final['type.name'] == 'Shot']['shot.end_location']]

    # Drop those column now that we have moved the data elsewhere.
    final.drop(['location', 'pass.end_location','carry.end_location', 'shot.end_location'], axis=1, inplace=True)


    final.to_csv('messi_events.csv')
        
    