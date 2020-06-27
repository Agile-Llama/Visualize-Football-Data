# Stats from StatsBomb free datasets

from data_functions import FreeCompetitions, FreeMatches
import pandas as pd

# Refer to page 19 of Open events for guide on shots.
# Types of shot:
    # 61 / “Corner”
    # 62 / “Free Kick” 
    # 87 / “Open Play” 
    # 88 / “Penalty” 
    # 65 / “Kick Off”

# Outcome of shot (shot.end_location)
    # 96 / “Blocked”
    # 97 / “Goal” 
    # 98 / “OffT” 
    # 99 / “Post”
    # 100 / “Saved”
    # 115 / “Saved Off T” 
    # 116 / “Saved To Post”

# Refer to page 18 and page 2 for info.
# end_location Where the shot ended.
    # can have x,y or x,y,z values.


# Shot numbers which I care about currently are:
    # 62 for free kicks.
    # 88 for penalties

# Full name
messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'messi_events.csv'

laliga_csv_file = 'laliga_events.csv'


# Currently only concerned with Messi stats. 
# Can expand later.
def main():
    # Load the csv file which has all the data pre processed
    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # Get all the goals that messi has scored. 
    # goals_by_game = df_messi[(df_messi['shot.outcome.name'] == 'Goal') & (df_messi['player.name'] == messi_name)].groupby('match_id')['player.name'].count()

    # Get all the pens scored.
    pens_scored = df_messi[(df_messi['shot.type.name'] == 'Penalty') & (df_messi['player.name'] == messi_name) & (df_messi['shot.outcome.name'] == 'Goal')]

    # All free kicks taken by Messi
    all_free_kicks = df_messi[(df_messi['shot.type.name'] == 'Free Kick') & (df_messi['player.name'] == messi_name)]

    free_kicks_blocked = all_free_kicks[(df_messi['shot.outcome.name'] == 'Blocked')]

    pd.set_option('display.max_rows', df_messi.shape[0]+1)

    print(free_kicks_blocked)



if __name__ == '__main__':
    main()





