# Stats from StatsBomb free datasets

from data_functions import FreeCompetitions, FreeMatches, StatsBombFreeEvents
import pandas as pd

# Full name
messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

file_to_load = 'df_messi'

# Post process the dataframe. Add and remove columns to streamline for later functions.
# Call this after creating the respective CSV file.
def post_process():

    free_comp = FreeCompetitions()
    messi_data = FreeMatches(free_comp[free_comp.competition_id == 11].reset_index())

    df_messi = StatsBombFreeEvents(messi_data)

    df_messi.reset_index(inplace=True, drop=True)

    df_messi['time'] = ( df_messi['minute'] * 60 + df_messi['second'] ) / 60

    df_messi[df_messi['location'].notnull()].head()

    # Create column for location_x, location_y
    df_messi.loc[df_messi['location'].notnull(),
              'location_x'] = [x[0] for x in df_messi[df_messi['location'].notnull()]['location']]
    df_messi.loc[df_messi['location'].notnull(),
              'location_y'] = [x[1] for x in df_messi[df_messi['location'].notnull()]['location']]

    # Create column for end_location
    # For pass
    df_messi.loc[df_messi['type.name'] == 'Pass',
             'end_location_x'] = [x[0] for x in df_messi[df_messi['type.name'] == 'Pass'
                                                                 ]['pass.end_location']]
    df_messi.loc[df_messi['type.name'] == 'Pass',
             'end_location_y'] = [x[1] for x in df_messi[df_messi['type.name'] == 'Pass'
                                                                 ]['pass.end_location']]
                                            
    df_messi.loc[df_messi['type.name'] == 'Carry',
             'end_location_x'] = [x[0] for x in df_messi[df_messi['type.name'] == 'Carry'
                                                                 ]['carry.end_location']]
    df_messi.loc[df_messi['type.name'] == 'Carry',
             'end_location_y'] = [x[1] for x in df_messi[df_messi['type.name'] == 'Carry'
                                                                  ]['carry.end_location']]
                                                    
    # For Shot
    df_messi.loc[df_messi['type.name'] == 'Shot',
             'end_location_x'] = [x[0] for x in df_messi[df_messi['type.name'] == 'Shot'
                                                                 ]['shot.end_location']]
    df_messi.loc[df_messi['type.name'] == 'Shot',
             'end_location_y'] = [x[1] for x in df_messi[df_messi['type.name'] == 'Shot'
                                                                 ]['shot.end_location']]
                                                    
    df_messi.drop(['location', 'pass.end_location','carry.end_location', 'shot.end_location'],
              axis=1,
              inplace=True)
    
    df_messi.to_csv('df_messi.csv')


if __name__ == '__main__':
    post_process()





