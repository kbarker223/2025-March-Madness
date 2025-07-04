from MM2025_Data_Loader import *
from MM2025_Classes import *
import pandas as pd
from itertools import combinations


#Build Functions

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

    if(team1.is_mens == True):
        gender = "Mens"
    else:
        gender = "Womens"

    return game_df, year, team1, team2, gender


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


def get_strength_of_schedule(year, team, gender):
    ##year is the year that we are calculating the schedule
    ##team is the team we want to check their SOS

    ## Formula:
    ## (2*(owp) + 1*(oowp))/3
    
    ## check if the teams are mens teams and get the data from m_...
    if(gender == "Mens"):
            
        # Filter data for the given season once
        season_games = m_regseason_stats[m_regseason_stats["GameID"].str.startswith(f"{year}_")].copy()

    ##check if the teams are womens team and then get the data from w_reg...
    elif(gender == "Womens"):
        # Filter data for the given season once
        season_games = w_regseason_stats[w_regseason_stats["GameID"].str.startswith(f"{year}_")].copy()
    else:
        print("Team not mens or womens")
        return -1

    ##now proceed to get the SOS

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


def win_pcnt(year, team, gender):
    """Returns float between 0 and 1 for the percentage of games won over a given season. 
    Computed by summing all wins divided by games played"""
    ##year is the year that we are calculating the schedule
    ##team is the team we want to check their SOS
    if(gender == "Mens"):
        #need to just get the id now, no longer a class object
        season_games = m_regseason_stats[m_regseason_stats["GameID"].str.contains(f"{year}_{team}") | 
                                         m_regseason_stats["GameID"].str.contains(f"{year}"f"_{team}")].copy()
    elif(gender == "Womens"):
        #need to just get the id now, no longer a class object
        season_games = w_regseason_stats[w_regseason_stats["GameID"].str.contains(f"{year}_{team}") | 
                                         w_regseason_stats["GameID"].str.contains(f"{year}"f"_{team}")].copy()
    else:
        print("Team not mens or womens")
        return -1
    
    wins = len(season_games[season_games["WTeamID"] == team])
    total_games = len(season_games[season_games["GameID"].str.contains(f"_{team}")])

    if(total_games == 0):
        return 0
    else:
        win_pct = wins/total_games
        return win_pct


def average_strength_of_schedule(year, gender):
    """Returns the average strength of schedule between all teams in NCAA for a 
    given year. Computed by finding strenght of schedule for every team, sum them
    all up, and divide by total number of teams in NCAA. 
    Helper function for matchup_prob"""     

    #might have to change how we handle mens or womens here
    if(gender == "Mens"):
        season_games = m_regseason_stats[m_regseason_stats["GameID"].str.contains(f"{year}")]
    elif(gender == "Womens"):
        season_games = w_regseason_stats[w_regseason_stats["GameID"].str.contains(f"{year}")]
    else:
        print("Team not mens or womens")
        return -1
    
    # get all the teams from the season
    unique_teams = set(season_games["WTeamID"]).union(set(season_games["LTeamID"]))

    # make a df of each teams SOS
    sos_values = [get_strength_of_schedule(year, team_id, gender) for team_id in unique_teams]

    # return average sos for a season
    return np.mean(sos_values)


def matchup_prob(year, team1, team2, gender, avg_sos):
    """Returns (list) with entries summing to 1 where the first entry is the
    respective probability team1 wins compared to team2"""

    ###We will most likely want to make year 2025 since the current season would be the
    # best predictor of their performance in the tournament, but leaving it a variable
    #in case we want to use it to test a model where we know tournament winners for 
    #previous years 


    weighted_win_pcnt1 = win_pcnt(year, team1, gender) * ( get_strength_of_schedule(year, team1, gender) / 
                                     avg_sos )
    
    weighted_win_pcnt2 = win_pcnt(year, team2, gender) * ( get_strength_of_schedule(year, team2, gender) / 
                                     avg_sos )
    
    total = weighted_win_pcnt1 + weighted_win_pcnt2

    prob_of_win_team1 = weighted_win_pcnt1 / total
    #prob_of_win_team2 = weighted_win_pcnt2 / total

    #not sure if its best to return prob_of_win_team1 and then you could get the 
    #prob of win for team2 by subracting 1 - prob_of_win_team1
    #OR we could return list or tuple with both probabilities

    return prob_of_win_team1

def to_betting_odds(year, team1, team2, gender):
    """If we want to use the go_to_converter, we need to change the implied 
    probabilities received by matchup_prob to gambling odds format.
    This is done by just taking the reciprocal of implied probabilities
    (gambling odds is the expected payout you get based on the prob
    of winning. If a team has 10% (.1) chance of winning then the expected
    payoff is 1/.1 = 10 meaning you get 10 times what you paid."""

    betting_odds_vector = [1 / p for p in matchup_prob(year, team1, team2, gender)]
    return betting_odds_vector




#These next functions are from goto-Conversion respository on GitHub
def convertAmericanOdds(listOfOdds):
    try: #using numpy
        listOfOdds = listOfOdds.astype(float)
        isNegativeAmericanOdds = listOfOdds < 0.0
        listOfOdds[isNegativeAmericanOdds] = 1.0 + ((100.0 / listOfOdds[isNegativeAmericanOdds]) * -1.0)
        listOfOdds[~isNegativeAmericanOdds] = 1.0 + (listOfOdds[~isNegativeAmericanOdds] / 100.0)
    except: #using base python
        for i in range(len(listOfOdds)):
            currOdds = listOfOdds[i]
            isNegativeAmericanOdds = currOdds < 0.0
            if isNegativeAmericanOdds:
                currDecimalOdds = 1.0 + (100.0/(currOdds*-1.0))
            else: #Is non-negative American Odds
                currDecimalOdds = 1.0 + (currOdds/100.0)
            listOfOdds[i] = currDecimalOdds
    return listOfOdds

def errorCatchers(listOfOdds):
    if len(listOfOdds) < 2:
        raise ValueError('len(listOfOdds) must be >= 2')
    try:
        isAllOddsAbove1 = np.all(listOfOdds > 1.0)
    except:
        isAllOddsAbove1 = all([x > 1.0 for x in listOfOdds])
    if not isAllOddsAbove1:
        raise ValueError('All odds must be > 1.0, set isAmericanOdds parameter to True if using American Odds')

def efficient_shin_conversion(listOfOdds, total = 1.0, multiplicativeIfUnprudentOdds = False, isAmericanOdds = False):

    #Convert American Odds to Decimal Odds
    if isAmericanOdds:
        listOfOdds = convertAmericanOdds(listOfOdds)

    #Error Catchers
    errorCatchers(listOfOdds)

    try: #using numpy
        #Compute parameters
        listOfPies = 1.0 / listOfOdds
        beta = np.sum(listOfPies)
        listOfComplementPies = listOfPies - (beta - listOfPies)

        #Compute vectors
        listOfZ = ((beta - 1.0) * (listOfComplementPies ** 2.0 - beta)) / (beta * (listOfComplementPies ** 2.0 - 1.0))
        listOfPStars = ((np.sqrt(listOfZ**2.0 + 4.0 * (1.0 - listOfZ) * (listOfPies**2 / beta)) - listOfZ) / (2.0 * (1.0 - listOfZ)))
        normalizer = np.sum(listOfPStars) / total
        outputListOfProbabilities = listOfPStars / normalizer

    except: #using base python
        #Compute parameters
        listOfPies = [1.0/x for x in listOfOdds]
        beta = sum(listOfPies)
        listOfComplementPies = [x - (beta-x) for x in listOfPies]

        #Compute vectors
        listOfZ = [((beta - 1.0)*(x**2.0 - beta))/(beta*(x**2.0 - 1.0)) for x in listOfComplementPies]
        listOfPStars = [(((z_i**2.0 + 4.0*(1.0-z_i)*(pi_i**2.0/beta))**0.5) - z_i)/(2.0*(1.0 - z_i)) for pi_i,z_i in zip(listOfPies, listOfZ)]
        normalizer = sum(listOfPStars)/total
        outputListOfProbabilities = [x/normalizer for x in listOfPStars]

    return outputListOfProbabilities

## https://www.kaggle.com/code/kaito510/goto-conversion-winning-solution -- goto conversion solution
def goto_conversion(listOfOdds, total = 1.0, multiplicativeIfUnprudentOdds = False, isAmericanOdds = False):

    #Convert American Odds to Decimal Odds
    if isAmericanOdds:
        listOfOdds = convertAmericanOdds(listOfOdds)

    #Error Catchers
    errorCatchers(listOfOdds)

    try: #using numpy
        listOfProbabilities = 1.0 / listOfOdds
        listOfSe = np.sqrt((listOfProbabilities - listOfProbabilities**2.0) / listOfProbabilities)
        step = (np.sum(listOfProbabilities) - total) / np.sum(listOfSe)
        outputListOfProbabilities = listOfProbabilities - (listOfSe * step)
        if np.any(outputListOfProbabilities <= 0.0) or (np.sum(listOfProbabilities) <= 1.0):
            if multiplicativeIfUnprudentOdds:
                normalizer = np.sum(listOfProbabilities) / total
                outputListOfProbabilities = np.array(listOfProbabilities) / normalizer
            else:
                print('Odds must have a positive low bookmaker margin to be prudent.')
                raise ValueError('Set multiplicativeIfUnprudentOdds argument to True to use multiplicative conversion for unprudent odds.')

    except: #using base python
        listOfProbabilities = [1.0/x for x in listOfOdds] #initialize probabilities using inverse odds
        listOfSe = [pow((x-x**2.0)/x,0.5) for x in listOfProbabilities] #compute the standard error (SE) for each probability
        step = (sum(listOfProbabilities) - total)/sum(listOfSe) #compute how many steps of SE the probabilities should step back by
        outputListOfProbabilities = [x - (y*step) for x,y in zip(listOfProbabilities, listOfSe)]
        if any(0.0 >= x for x in outputListOfProbabilities) or (sum(listOfProbabilities) <= 1.0):
            if multiplicativeIfUnprudentOdds:
                normalizer = sum(listOfProbabilities)/total
                outputListOfProbabilities = [x/normalizer for x in listOfProbabilities]
            else:
                print('Odds must have a positive low bookmaker margin to be prudent.')
                raise ValueError('Set multiplicativeIfUnprudentOdds argument to True to use multiplicative conversion for unprudent odds.')

    return outputListOfProbabilities

def zero_sum(listOfPrices, listOfVolumes):
    listOfSe = [x**0.5 for x in listOfVolumes] #compute standard errors assuming standard deviation is same for all stocks
    step = sum(listOfPrices)/sum(listOfSe)
    outputListOfPrices = [x - (y*step) for x,y in zip(listOfPrices, listOfSe)]
    return outputListOfPrices


def generate_matchups(year, gender):
    if(gender == "Mens"):
        season_games = m_regseason_stats[m_regseason_stats["GameID"].str.contains(f"{year}")]
    elif(gender == "Womens"):
        season_games = w_regseason_stats[w_regseason_stats["GameID"].str.contains(f"{year}")]
    else:
        print("Team not mens or womens")
        return -1
    
    unique_teams = set(season_games["WTeamID"]).union(set(season_games["LTeamID"]))
    matchups = [(f"{year}_{team1}_{team2}") for team1, team2 in combinations(sorted(unique_teams), 2)]
    
    matchups_df = pd.DataFrame(matchups, columns=["GameID"])
    matchups_df[["Year", "Team1", "Team2"]] = matchups_df["GameID"].str.split("_", expand=True)
          
    return matchups_df

def predict_games(matchups_list, gender, avg_sos):
    # Select the first row of the DataFrame
    row = matchups_list.iloc[0]
    # Print the information for this row
    print(f"Processing Year: {row['Year']}, Team1: {row['Team1']}, Team2: {row['Team2']}")

    # Call the prediction function for this single row
    prediction = matchup_prob(
        int(row["Year"]), 
        int(row["Team1"]), 
        int(row["Team2"]), 
        gender, 
        avg_sos
    )

    # Print the prediction
    print(f"Prediction: {prediction}")

    # Return the output (GameID and Prediction)
    return row["GameID"], float(prediction)
