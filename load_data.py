# Stats from StatsBomb free datasets

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


import pandas as pd

from data_functions import FreeMatches, FreeCompetitions, StatsBombFreeEvents

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

free_comp = FreeCompetitions()
messi_data = FreeMatches(free_comp[free_comp.competition_id == 11].reset_index())

# Running this will take about 8-10mins
df_messi = StatsBombFreeEvents(messi_data)

# Writing to csv file takes about 
df_messi.to_csv('df_messi.csv')