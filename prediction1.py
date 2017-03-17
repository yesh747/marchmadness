#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 16:31:47 2017

@author: Yesh
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
year = 2017

datasets = [season, tourneySeeds, tourneySlots]
# Create 2017 season dataframe
i = 0
for dataset in datasets:
    print(dataset.shape)
    datasets[i] = dataset[dataset['Season'] == year]
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
seasonGroup = seasonTourney2017.groupby(['Wteam','Lteam','Daynum', 'Season']).aggregate(np.mean).reset_index()

tourneyTeam2017 = None
seasonTourney2017 = None


#==============================================================================
# Compare two teams based on season history
#==============================================================================

def comparator(team1str, team2str):

    team1Wscore = 0
    team2Wscore = 0
    team1Lscore = 0
    team2Lscore = 0
    
    team1 = teams[teams['Team_Name'] == team1str]['Team_Id'].iloc[0]
    team2 = teams[teams['Team_Name'] == team2str]['Team_Id'].iloc[0]


    seasonGroupWTeam = seasonGroup.groupby('Wteam').aggregate(np.mean).reset_index()
    team1Wscore = seasonGroupWTeam['Wscore'][seasonGroupWTeam['Wteam'] == team1].iloc[0]
    team2Wscore = seasonGroupWTeam['Wscore'][seasonGroupWTeam['Wteam'] == team2].iloc[0]
    
    seasonGroupLTeam = seasonGroup.groupby('Lteam').aggregate(np.mean).reset_index()
    
    if (seasonGroupLTeam['Lscore'][seasonGroupLTeam['Lteam'] == team1].empty != True)  & (seasonGroupLTeam['Lscore'][seasonGroupLTeam['Lteam'] == team2].empty != True):
        team1Lscore = seasonGroupLTeam['Lscore'][seasonGroupLTeam['Lteam'] == team1].iloc[0]
        team2Lscore = seasonGroupLTeam['Lscore'][seasonGroupLTeam['Lteam'] == team2].iloc[0]
    
    index = (team1Wscore - team2Wscore) + (team1Lscore - team2Lscore)
    
    return index
    

comparator("Gonzaga", "S Dakota St")


#==============================================================================
# Work through the tournament
#
# R1 to R6
# 4 Regions: W, X, Y, Z -> (East, Midwest, South, West)
#==============================================================================

tourneySeeds2017['Seed'].replace(to_replace='W11b', value='W11', inplace=True)
tourneySeeds2017['Seed'].replace(to_replace='W16b', value='W16', inplace=True)
tourneySeeds2017['Seed'].replace(to_replace='Y16b', value='Y16', inplace=True)
tourneySeeds2017['Seed'].replace(to_replace='Z11a', value='Z11', inplace=True)
 
# level is the round of the tourny
def predictRound(region, level):
    region = region
    level = level
    tourneyRound = tourneySlots2017[tourneySlots2017['Slot'].str.contains(level+region)]
    
    for index, game in tourneyRound.iterrows():
        team1Seed = game['Strongseed']
        team2Seed = game['Weakseed']
        team1Id = tourneySeeds2017[tourneySeeds2017['Seed'] == team1Seed]['Team'].iloc[0]
        team2Id = tourneySeeds2017[tourneySeeds2017['Seed'] == team2Seed]['Team'].iloc[0]
        team1Name = teams[teams['Team_Id'] == team1Id]['Team_Name'].iloc[0]
        team2Name = teams[teams['Team_Id'] == team2Id]['Team_Name'].iloc[0]
        
        index = comparator(team1Name, team2Name)
        
        if index > 0:
            print(team1Name, 'beats', team2Name, 'in Region', region, 'Round', level)
            print('-'*50)
        elif index < 0:
            print(team2Name, 'beats', team1Name, 'in Region', region, 'Round', level )
            print('-'*50)
        elif index == 0:
            print('higher seed team wins')
            print('-'*50)


predictRound('W', 'R1')
print('='*50)
predictRound('X', 'R1')
print('='*50)
predictRound('Y', 'R1')
print('='*50)
predictRound('Z', 'R1')


# TODO:
#    1. Finish bracket solver generator.
#    2. Test algorithm on previous years.
#    3. Try and learn some scikit-learn stuff


