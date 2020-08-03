from data_functions import compute_defensive_actions
import pandas as pd

# Referncing https://statsbomb.com/2014/07/defensive-metrics-measuring-the-intensity-of-a-high-press/

# The idea of this function is to get an indication of how much pressing was done in a given game.

#The defensive actions that I am using are the following four Opta defined events:

    # Tackles
    # Interceptions
    # Challenges (failed tackles)
    # Fouls

# The final formula is PPDA = Number of Passes made by Attacking Team / Number of Defensive Actions
# A smaller PPDA value signifies a greater level of defensive intensity, 
# as in essence, the defence has allowed a smaller ratio of uncontested passes to be made.

messi_name = 'Lionel Andrés Messi Cuccittini'

laliga_id = 11

messi_csv_file = 'df_messi.csv'

def calculate_PPDA(match_id):
    df_messi = pd.read_csv(messi_csv_file, index_col=0, low_memory=False)

    # Defensive aactions both teams
    def_actions = compute_defensive_actions(df_messi, match_id)

    # total passes by attacking team
    total_passes = df_messi[(df_messi['match_id'] == match_id) & (df_messi['type.name'] == 'Pass') & (df_messi['team.name'] == 'Barcelona')].shape[0]

    print(total_passes)
    print(def_actions)
        

if __name__ == '__main__':
    calculate_PPDA(69213)
