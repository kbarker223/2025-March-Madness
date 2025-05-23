import numpy as np
import pandas as pd
from sklearn.metrics import brier_score_loss, mean_squared_error



# Load the data
m_teams = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\MTeams.csv')
w_teams = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\WTeams.csv')

m_tourneyseed = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\MNCAATourneySeeds.csv')
w_tourneyseed = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\WNCAATourneySeeds.csv')

m_rs_stats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\MRegularSeasonDetailedResults.csv')
w_rs_stats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\WRegularSeasonDetailedResults.csv')

m_tstats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\MNCAATourneyDetailedResults.csv')
w_tstats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\WNCAATourneyDetailedResults.csv')

m_regseason_stats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\m_regseason_stats_w_ids.csv')
w_regseason_stats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\w_regseason_stats_w_ids.csv')

m_tourney_stats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\m_tourney_stats_w_ids.csv')
w_tourney_stats = pd.read_csv('C:\\Users\\kaian\\OneDrive\\Desktop\\Kaggle 2025 MM Comp\\Data MM25\\w_tourney_stats_w_ids.csv')

# m_seed = pd.read_csv('/kaggle/input/march-machine-learning-mania-2025/MNCAATourneySeeds.csv')
# seed_df = pd.concat([m_seed, w_seed], axis=0).fillna(0.05)
# submission_df = pd.read_csv('/kaggle/input/march-machine-learning-mania-2025/SampleSubmissionStage1.csv')

