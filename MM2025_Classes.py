from MM2025_Data_Loader import *
from MM2025_Functions import *

class Team:
    def __init__(self, team_id):
        self.team_id = team_id
        self.is_mens = False
        self.is_womens = False
        self.team_name = "NA"
        
        if (team_id in m_teams["TeamID"].to_list()):
            self.is_mens = True
        elif (team_id in w_teams["TeamID"].to_list()):
            self.is_womens = True
        else:
            print("Invalid Team ID")

        
        ## get the teams name
        if (self.is_mens == True):
            self.team_name = m_teams[m_teams["TeamID"] == self.team_id]["TeamName"].values[0]
        elif (self.is_womens == True):
            self.team_name = w_teams[w_teams["TeamID"] == self.team_id]["TeamName"].values[0]
        else:
            return -1


        
