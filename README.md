Using public statsbomb dataset. This dataset can be found here https://github.com/statsbomb/open-data.

The dataset includes matches from many compeitions including the womens world cup. Im focusing on the data which feature on Lionel Messi.

Functions:

    load_data.py - Call the function 'all_events()' to get a csv file with all the data which is required for all other functions. File name is 'df_messi.csv'

    data_functions.py - Has a bunch of useful functions which other files use. Never really need to interact with it directly. 

    heatmap.py - Creates a heatmap for a given season. Only for Lionel Messi atm. (Either highest/lowest Expected goal game)
        -Saves into Heatmaps/Lowest_xG or Heatmaps/Highest_xG

    passmap.py - Creates a passmap for a given season. Only for Lionel Messi atm. (Either highest/lowest Expected goal game)
        -Saves into Passmaps/Lowest_xG or Passmaps/Highest_xG

    defensive_visualisation.py - Currently not working. Idea is to get average of all defence accross a season then checks a specific game to see if its greater or less than the mean defence. Then create a defensive pressure map.

df_messi.csv - Can be generated through functions provided(load_data.py). However, the file is provided in this repo. About 700mb download though.

Passmap/heatmap images for all seasons in their respective folders.
