from MM2025_Functions import *
from MM2025_Code import *
from MM2025_Classes import *

## only needs to be ran one time
'''
add_game_ids(m_regseason_stats, "m_regseason_stats_w_ids.csv")
add_game_ids(w_regseason_stats, "w_regseason_stats_w_ids.csv")
add_game_ids(m_tourney_stats, "m_tourney_stats_w_ids.csv")
add_game_ids(w_tourney_stats, "w_tourney_stats_w_ids.csv")
'''

## test last n games
#id_str = "2014_1101_1146"
#team_matchup, year, team1, team2, gender = extract_game_info(id_str)
#avg = average_strength_of_schedule(year, gender)
#print(avg)

#avg_sos = average_strength_of_schedule(2025, "Mens")
#print(avg_sos)
matchups_2025 = generate_matchups(2025, "Mens")

games = predict_games(matchups_2025, "Mens", 0.4974665931234844)
print(games)
'''
Processing Year: 2025, Team1: 1101, Team2: 1438
'''

# print(get_last_n_games(team_matchup, 1101, 10))
# print(m_teams[m_teams["TeamID"] == 1146])
# print(win_pcnt("2014", team2))

#print(matchup_prob(year, team1, team2, gender))
#team_id = 1101
#team1 = Team(team_id=team_id)
#print(determine_wl(team1))

##team_matchup
# id_str = "2014_1101_1146"
# team_matchup = extract_game_info(id_str)
# print(team_matchup)
#print(determine_wl(team_matchup))
# print("############################")
#print(m_regseason_stats[m_regseason_stats["Season"] == int(team_matchup["year"])][m_regseason_stats["LTeamID"] == int(team_matchup["team1_id"])][m_regseason_stats["WTeamID"] == int(team_matchup["team2_id"])])


