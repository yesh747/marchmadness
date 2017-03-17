# -*- coding: utf-8 -*-
"""
Title: Sandbox
Author: Yeshwant Chillakuru
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

teams = pd.read_csv("/Users/Yesh/Documents/workspace/MarchMadnessPrediction/data/Teams.csv")
season = pd.read_csv("/Users/Yesh/Documents/workspace/MarchMadnessPrediction/data/RegularSeasonDetailedResults.csv")
tourneySeeds = pd.read_csv("/Users/Yesh/Documents/workspace/MarchMadnessPrediction/data/TourneySeeds.csv")
tourneySlots = pd.read_csv("/Users/Yesh/Documents/workspace/MarchMadnessPrediction/data/TourneySlots.csv")


# ----------------------------------------------------------------------
# 2017 only


datasets = [season, tourneySeeds, tourneySlots]
# Create 2017 season dataframe
i = 0
for dataset in datasets:
    print(dataset.shape)
    datasets[i] = dataset[dataset['Season'] == 2017]
    print(dataset.shape)
    season2017 = datasets[0]
    tourneySeeds2017 = datasets[1]
    tourneySlots2017 = datasets[2]
    i = i+1
i = None
datasets = None
dataset = None

tourneyTeam2017 = tourneySeeds2017["Team"]
seasonTourney2017 = season2017[season2017['Wteam'].isin(tourneyTeam2017)]
seasonTourneyGroup2017 = seasonTourney2017.groupby(['Wteam','Lteam','Daynum', 'Season']).aggregate(np.mean).reset_index()


# Merge with team names
seasonGroup2017 = seasonTourneyGroup2017.merge(teams, how="inner", left_on='Wteam', right_on='Team_Id')

tourneyTeam2017 = None
seasonTourney2017 = None
seasonTourneyGroup2017 = None




# ---------------------------------------------------------------
# Analysis from 2010 to 2017

tourneyTeam = tourneySeeds["Team"]
seasonTourney = season[season['Wteam'].isin(tourneyTeam)]
seasonTourneyGroup = seasonTourney.groupby(['Wteam','Lteam','Daynum', 'Season']).aggregate(np.mean).reset_index()

# Drop data from before 2015
seasonTourneyGroup['Season'] = pd.to_numeric(seasonTourneyGroup['Season'])
seasonGroup = seasonTourneyGroup[seasonTourneyGroup['Season'] >= 2013]


## clean workspace
tourneyTeam = None
seasonTourney = None





#==============================================================================
# See if any Wteams have been defeated by an Lteam which they have beaten.
# - Logic: for each Wteam-Lteam pair(1), check if Lteam(1) is elsewhere a 
#       Wteam(2) thaat betas a losing team (2)
#==============================================================================
#
#uniqueWteams = seasonTourneyGroup['Wteam'].unique()
#uniqueLteams = seasonTourneyGroup['Lteam'].unique()
#
#losingTeamsThatCameBackToBeatWinningTeams = []

## loop through unqiue winning teams
#for wteam in uniqueWteams:
#    for index, row in seasonTourneyGroup.iterrows(): 
#        
#        # for each instance of a unique winning team (wteam), find its corresponding losing team (lteam)
#        if (row['Wteam'] == wteam):
#            lteam = row['Lteam']
#            
#            # Iterate over rows where lteam was a winner
#            for index, row in seasonTourneyGroup[seasonTourneyGroup['Wteam'] == lteam].iterrows():
#                
#                # Check to see if lteam ever beat wteam
#                if (row['Lteam'] == wteam):
#                    losingTeamsThatCameBackToBeatWinningTeams.append(lteam)
#                
#
#wteam = None
#lteam = None
#index = None
#row = None



#==============================================================================
# Examine Tournamet Comparison
#==============================================================================

# Compare 2 teams that have close seeding based on average win and loss scores

def comparator(team1str, team2str):
    team1 = teams[teams['Team_Name'] == team1str]['Team_Id'].iloc[0]
    team2 = teams[teams['Team_Name'] == team2str]['Team_Id'].iloc[0]
    seasonGroup_matchup = seasonGroup.loc[((seasonGroup['Wteam'] == team1) | (seasonGroup['Lteam']==team1)) & ((seasonGroup['Wteam'] == team2) | (seasonGroup['Lteam']==team2))]
    season_matchup = season.loc[((season['Wteam'] == team1) | (season['Lteam']==team1)) & ((season['Wteam'] == team2) | (season['Lteam']==team2))]
    
    print(seasonGroup_matchup)
    print(season_matchup)
    
    seasonGroupWTeam = seasonGroup.groupby('Wteam').aggregate(np.mean).reset_index()
    team1Wscore = seasonGroupWTeam['Wscore'][seasonGroupWTeam['Wteam'] == team1].iloc[0]
    team2Wscore = seasonGroupWTeam['Wscore'][seasonGroupWTeam['Wteam'] == team2].iloc[0]
    
    seasonGroupLTeam = seasonGroup.groupby('Lteam').aggregate(np.mean).reset_index()
    team1Lscore = seasonGroupLTeam['Lscore'][seasonGroupLTeam['Lteam'] == team1].iloc[0]
    team2Lscore = seasonGroupLTeam['Lscore'][seasonGroupLTeam['Lteam'] == team2].iloc[0]
    
    print('Team 1\'s win score average is: ', team1Wscore, '. ')
    print('Team 2\'s win score average is: ', team2Wscore, '. ')
    
    print('Team 1\'s lose score average is: ', team1Lscore, '. ')
    print('Team 2\'s lose score average is: ', team2Lscore, '. ')
    
    print('Team1 vs Team2 index: ', (team1Wscore - team2Wscore) + (team1Lscore - team2Lscore))
    


comparator('Virginia', 'Florida')

comparator('Baylor', 'Duke')

comparator('Northwestern', 'Vanderbilt')

comparator('Villanova','Duke')

comparator('Notre Dame','West Virginia')

comparator('Maryland','Florida St')

comparator('Arizona','Florida St')

comparator('Gonzaga','Arizona')

comparator('Arizona','Duke')

comparator('Miami FL','Michigan St')

comparator('Iowa St','Purdue')

comparator('Kansas','Iowa St')

comparator('Creighton','Rhode Island')

comparator('Creighton','Oregon')

comparator('Creighton','Louisville')

comparator('Creighton','Iowa St')

comparator('Michigan','Oklahoma St')

comparator('Arkansas','Seton Hall')

comparator('Minnesota','Butler')

comparator('North Carolina','Minnesota')

comparator('Cincinnati','UCLA')

comparator('UCLA','Kentucky')

comparator('Dayton','Wichita St')

comparator('North Carolina','UCLA')

comparator('Iowa St','UCLA')

comparator('Iowa St','Duke')



comparator('Virginia Tech','Florida')







