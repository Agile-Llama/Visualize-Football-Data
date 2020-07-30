# Stats from StatsBomb free datasets
import pandas as pd
from data_functions import FreeMatches, FreeCompetitions, StatsBombFreeEvents

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

free_comp = FreeCompetitions()

# kinda redundant for the moment.
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


def all_events():
    """
        Function to get all the events from all laliga seasons.
        Writes these events to a csv file called 'df_messi.csv'
    """
    free_comp = FreeCompetitions()
    messi_data = FreeMatches(free_comp[free_comp.competition_id == 11].reset_index())

    df_messi = StatsBombFreeEvents(messi_data)

    df_messi.reset_index(inplace=True, drop=True)

    df_messi['time'] = ( df_messi['minute'] * 60 + df_messi['second'] ) / 60

    df_messi[df_messi['location'].notnull()].head()

    # Create column for location_x, location_y
    df_messi.loc[df_messi['location'].notnull(), 'location_x'] = [x[0] for x in df_messi[df_messi['location'].notnull()]['location']]
    df_messi.loc[df_messi['location'].notnull(), 'location_y'] = [x[1] for x in df_messi[df_messi['location'].notnull()]['location']]

    # Create column for end_location
    # For pass
    df_messi.loc[df_messi['type.name'] == 'Pass', 'end_location_x'] = [x[0] for x in df_messi[df_messi['type.name'] == 'Pass' ]['pass.end_location']]
    df_messi.loc[df_messi['type.name'] == 'Pass', 'end_location_y'] = [x[1] for x in df_messi[df_messi['type.name'] == 'Pass' ]['pass.end_location']]

    # For carry                                
    df_messi.loc[df_messi['type.name'] == 'Carry', 'end_location_x'] = [x[0] for x in df_messi[df_messi['type.name'] == 'Carry' ]['carry.end_location']]
    df_messi.loc[df_messi['type.name'] == 'Carry', 'end_location_y'] = [x[1] for x in df_messi[df_messi['type.name'] == 'Carry' ]['carry.end_location']]
                                                    
    # For Shot
    df_messi.loc[df_messi['type.name'] == 'Shot', 'end_location_x'] = [x[0] for x in df_messi[df_messi['type.name'] == 'Shot' ]['shot.end_location']]
    df_messi.loc[df_messi['type.name'] == 'Shot', 'end_location_y'] = [x[1] for x in df_messi[df_messi['type.name'] == 'Shot' ]['shot.end_location']]
                                                    
    df_messi.drop(['location', 'pass.end_location','carry.end_location', 'shot.end_location'], axis=1, inplace=True)
    
    df_messi.to_csv('df_messi.csv')

all_events()

        
    