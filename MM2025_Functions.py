from MM2025_Data_Loader import *
from MM2025_Classes import *
import pandas as pd

#Build Functions

from MM2025_Data_Loader import *
from MM2025_Classes import *
import pandas as pd

# Build Functions

# Generate GameID for each row
def generate_game_id(row):
    year = row["Season"]  # Assuming "Season" column stores the year
    team1_id, team2_id = sorted([row["WTeamID"], row["LTeamID"]])  # Ensure order
    return f"{year}_{team1_id}_{team2_id}"

def add_game_ids(dataframe, output_filename):
    ## one time use function
    ## only needs to be ran one time to 
    ## add a "GameID" column to appropriate csvs with 
    dataframe["GameID"] = dataframe.apply(generate_game_id, axis=1)
    
    cols = ['GameID'] + [col for col in dataframe.columns if col != 'GameID']
    dataframe = dataframe[cols]

    # Save back to CSV
    dataframe.to_csv(output_filename, index=False)

    print("GameID column successfully added")


## needed functions
def extract_game_info(id_str):
    parts = id_str.split('_')
    year = int(parts[0])
    team1_id = int(parts[1])
    team2_id = int(parts[2])

    # Ensure consistent ordering of team IDs
    team1_id, team2_id = sorted([team1_id, team2_id])

    team1 = Team(team_id=team1_id)
    team2 = Team(team_id=team2_id)

    # Create a unique game identifier
    game_id = f"{year}_{team1_id}_{team2_id}"

    game_df = pd.DataFrame([{
        'GameID': game_id,  # unique game id
        'year': year,
        'team1_id': team1.team_id,
        'team1_name': team1.team_name,
        'team2_id': team2.team_id,
        'team2_name': team2.team_name,
        'Male1': team1.is_mens,
        'Male2': team2.is_mens
    }])

    return game_df, team1, team2


def get_seed(team_id):
    if(int(team_id) - 1000 < 1000):
        return m_tourneyseed[m_tourneyseed["TeamID"] == team_id]["Seed"]
    if(int(team_id) - 1000 > 1000):
        return w_tourneyseed[w_tourneyseed["TeamID"] == team_id]["Seed"]
    else:
        print("Team ID not found")
        return -1
    
def get_regseason_stats(team):
    if(team.is_mens == True):
        return m_regseason_stats[m_regseason_stats["WTeamID"] == team.team_id], m_regseason_stats[m_regseason_stats["LTeamID"] == team.team_id]
    elif(team.is_womens == True):
        return m_regseason_stats[w_regseason_stats["WTeamID"] == team.team_id], w_regseason_stats[m_regseason_stats["LTeamID"] == team.team_id]
    else:
        return -1

def get_tourney_stats(team):
    if(team.is_mens == True):
        return m_tourney_stats[m_tourney_stats["WTeamID"] == team.team_id], m_tourney_stats[m_tourney_stats["LTeamID"] == team.team_id]

    elif(team.is_womens == True):
        return w_tourney_stats[m_tourney_stats["WTeamID"] == team.team_id], m_tourney_stats[w_tourney_stats["LTeamID"] == team.team_id]
    else:
        return -1

def determine_winner(game_info):
    team1 = game_info["team1_id"].values[0]
    team2 = game_info["team2_id"].values[0]
    winner = -1

    if(game_info["Male1"].values[0] == True and game_info["Male2"].values[0] == True):
        if(game_info["GameID"].values[0] in m_regseason_stats["GameID"].values):
            if(team1 == m_regseason_stats[m_regseason_stats["GameID"]== game_info["GameID"].values[0]]["WTeamID"].values[0]):
                winner = team1
                return winner
            else:
                winner = team2
                return winner
        
        ## check if it is a tournament game
        elif(game_info["GameID"].values[0] in m_tourney_stats["GameID"].values):
            if(team1 == m_tourney_stats[m_tourney_stats["GameID"]== game_info["GameID"].values[0]]["WTeamID"].values[0]):
                winner = team1
                return winner
            else:
                winner = team2
                return winner
        else:
            print("GameID not in Regular or Tournament")
            return -1
    
    ## check if it is a womens game

    ## check if it is a regular season game
    elif(game_info["Male1"].values[0] == False and game_info["Male2"].values[0] == False):
        if(game_info["GameID"].values[0] in w_regseason_stats["GameID"].values):
            if(team1 == w_regseason_stats[w_regseason_stats["GameID"]== game_info["GameID"].values[0]]["WTeamID"].values[0]):
                winner = team1
                return winner
            else:
                winner = team2
                return winner
        
        ## check if it is a tournament game
        elif(game_info["GameID"].values[0] in w_tourney_stats["GameID"].values):
            if(team1 == w_tourney_stats[w_tourney_stats["GameID"]== game_info["GameID"].values[0]]["WTeamID"].values[0]):
                winner = team1
                return winner
            else:
                winner = team2
                return winner
        else:
            print("GameID not in regular or tourney")
            return -1
        
    else:
        print("GameID not mens or womens")
        return -1
    

## get last n matchups
def get_last_n_matchups(game_info, n):
    team1 = game_info["team1_id"].values[0]
    team2 = game_info["team2_id"].values[0]

    ## check for mens
    if(game_info["Male1"].values[0] == True and game_info["Male2"].values[0] == True):
        reg = m_regseason_stats[m_regseason_stats["GameID"].str.contains(f"_{team1}_{team2}") | m_regseason_stats["GameID"].str.contains(f"_{team2}_{team1}")]
        tourney = m_tourney_stats[m_tourney_stats["GameID"].str.contains(f"_{team1}_{team2}") | m_tourney_stats["GameID"].str.contains(f"_{team2}_{team1}")]

        ## combine tourney and reg season
        combined_matchups = pd.concat([reg, tourney])
        filtered_df = combined_matchups.sort_values(by="GameID", ascending=False)

        return filtered_df.head(n)
    
    ## check for womens
    elif(game_info["Male1"].values[0] == False and game_info["Male2"].values[0] == False):
        reg = w_regseason_stats[w_regseason_stats["GameID"].str.contains(f"_{team1}_{team2}") | w_regseason_stats["GameID"].str.contains(f"_{team2}_{team1}")]
        tourney = m_tourney_stats[w_tourney_stats["GameID"].str.contains(f"_{team1}_{team2}") | w_tourney_stats["GameID"].str.contains(f"_{team2}_{team1}")]

        ## combine tourney and reg season
        combined_matchups = pd.concat([reg, tourney])
        filtered_df = combined_matchups.sort_values(by="GameID", ascending=False)

        return filtered_df.head(n)


def get_last_n_games(game_info, team_id, n):
    team = team_id
    
    ## check for mens
    if(game_info["Male1"].values[0] == True and game_info["Male2"].values[0] == True):
        reg = m_regseason_stats[m_regseason_stats["GameID"].str.contains(f"_{team}_") | m_regseason_stats["GameID"].str.contains(f"_{team}")]
        tourney = m_tourney_stats[m_tourney_stats["GameID"].str.contains(f"_{team}_") | m_tourney_stats["GameID"].str.contains(f"_{team}")]

        combined_matchups = pd.concat([reg, tourney])
        filtered_df = combined_matchups.sort_values(by="GameID", ascending=False)
        
        return filtered_df.head(n)
    
    ## check for womens
    elif(game_info["Male1"].values[0] == False and game_info["Male2"].values[0] == False):
        reg = w_regseason_stats[w_regseason_stats["GameID"].str.contains(f"_{team}_") | w_regseason_stats["GameID"].str.contains(f"_{team}")]
        tourney = w_tourney_stats[w_tourney_stats["GameID"].str.contains(f"_{team}_") | w_tourney_stats["GameID"].str.contains(f"_{team}")]

        combined_matchups = pd.concat([reg, tourney])
        filtered_df = combined_matchups.sort_values(by="GameID", ascending=False)
        
        return filtered_df.head(n)


def get_strength_of_schedule(year, team):
    ## Formula:
    ## (2*(owp) + 1*(oowp))/3

    ## need to add for women (just an if statement)

    # Filter data for the given season once
    season_games = m_regseason_stats[m_regseason_stats["GameID"].str.startswith(f"{year}_")].copy()

    # Extract winning and losing teams
    win_counts = season_games.groupby("WTeamID").size()
    total_games = season_games.groupby("WTeamID").size().add(season_games.groupby("LTeamID").size(), fill_value=0)

    # Compute win percentages for all teams
    team_win_pct = (win_counts / total_games).fillna(0).to_dict()

    # Get games played by the team
    team_games = season_games[
        season_games["GameID"].str.startswith(f"{year}_{team}_") |
        season_games["GameID"].str.endswith(f"_{team}")
    ].copy()

    # Extract opponent team IDs
    team_games["Opponent"] = team_games["GameID"].apply(
        lambda x: x.split("_")[2] if x.split("_")[1] != team else x.split("_")[1]
    ).astype(int)

    # Calculate OWP (Opponent Win Percentage)
    owp = team_games["Opponent"].map(team_win_pct).mean()

    # Calculate OOWP (Opponent's Opponent Win Percentage)
    def get_opponents_opponent_win_pct(opp):
        opp_games = season_games[
            season_games["GameID"].str.startswith(f"{year}_{opp}_") |
            season_games["GameID"].str.endswith(f"_{opp}")
        ]
        opp_opponents = opp_games["GameID"].apply(
            lambda x: x.split("_")[2] if x.split("_")[1] == opp else x.split("_")[1]
        ).astype(int)
        return opp_opponents.map(team_win_pct).mean()

    oowp = team_games["Opponent"].apply(get_opponents_opponent_win_pct).mean()

    # Strength of Schedule Formula
    sos = (2 * owp + oowp) / 3
    return sos

def win_pcnt(year, team):
    """Returns float between 0 and 1 for the percentage of games won over a given season. 
    Computed by summing all wins divided by games played"""
    ...

def average_strength_of_schedule(year):
    """Returns the average strength of schedule between all teams in NCAA for a 
    given year. Computed by finding strenght of schedule for every team, sum them
    all up, and divide by total number of teams in NCAA. 
    Helper function for matchup_prob"""
    ...

def matchup_prob(year, team1, team2):
    """Returns (list) with entries summing to 1 where the first entry is the
    respective probability team1 wins compared to team2"""

    ###We will most likely want to make year 2025 since the current season would be the
    # best predictor of their performance in the tournament, but leaving it a variable
    #in case we want to use it to test a model where we know tournament winners for 
    #previous years 

    weighted_win_pcnt1 = win_pcnt(year, team1) * ( get_strength_of_schedule(year, team1) / 
                                     average_strength_of_schedule(year) )
    
    weighted_win_pcnt2 = win_pcnt(year, team2) * ( get_strength_of_schedule(year, team2) / 
                                     average_strength_of_schedule(year) )
    
    total = weighted_win_pcnt1 + weighted_win_pcnt2

    prob_of_win_team1 = weighted_win_pcnt1 / total
    prob_of_win_team2 = weighted_win_pcnt2 / total

    #not sure if its best to return prob_of_win_team1 and then you could get the 
    #prob of win for team2 by subracting 1 - prob_of_win_team1
    #OR we could return list or tuple with both probabilities

    return [prob_of_win_team1, prob_of_win_team2]