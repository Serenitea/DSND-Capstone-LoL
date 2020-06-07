import requests, json
import numpy as np
import importlib
import pandas as pd
import pickle
import os

import seaborn as sns
import matplotlib.pyplot as plt


def pkl_file(filename, filepath):
    '''
    Save a file named 'filename' to 'filepath' via the pickle module
    '''
    with open(filepath, 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(filename, filehandle)

def load_pkl(filepath):
    '''
    Load a file from 'filepath'
    '''
    with open(filepath, 'rb') as filehandle:
        # read the data as binary data stream
        return pickle.load(filehandle)

def save_txt(filename, filepath):
    '''
    Save a file named 'filename' to 'filepath' as a text file
    '''
    f = open(filepath,"w")
    f.write( filename )
    f.close()


def extract_match_results(gameId):
    '''
    extract post-game match results from match data saved in dict for each match ID
    parameters for each game:
        - winner (red or blue)
        - red or blue (or neither) for boolean parameters: 'firstTower', 'firstInhibitor', 'firstBaron', 'firstDragon', 
               'firstRiftHerald'
        - difference between each team for numerical parameters: 
        'baronKills', 'riftHeraldKills', 'dragonKills', number of dragon kills by type, dragon soul
'''
    match_detail = match_detail_dict[gameId] #retrieve game details from dict
    
    match_stats = {} #initialize dict for game
    #create a key for the game winner
    match_stats['GameDuration'] = match_detail['gameDuration']
    if match_detail['teams'][0]['win'] == 'Win':
        match_stats['Winner'] = 'blue' 
    elif match_detail['teams'][1]['win'] == 'Win':
        match_stats['Winner'] = 'red' 

    #store bool params in match details
    for param in bool_params:
        if match_detail['teams'][0][param] == True:
            match_stats[param] = 'blue'
        elif match_detail['teams'][1][param] == True:
            match_stats[param] = 'red'

    #store num params in match details
    for param in num_params:
        match_stats[param+'diff'] = match_detail['teams'][0][param] - match_detail['teams'][1][param]

    #make post-game objective df for determining whole-game elemental dragon and soul differences
    match_obj = create_obj_list(match_timeline_dict[gameId]['frames'])
    if len(match_obj) > 0: #check that the list of objectives is not empty
        obj_timeline_df = pd.DataFrame(match_obj)
        if obj_timeline_df[obj_timeline_df['ObjectiveType'] == 'DRAGON'].shape[0] > 0: #check that there are dragons in the objectives list
            drag_df = obj_timeline_df[obj_timeline_df['ObjectiveType'] == 'DRAGON'].reset_index() #slice df of dragons only
            for side in ['blue', 'red']: #does either side have soul
                    if drag_df.query('DragElement != "ELDER_DRAGON" and team == @side').shape[0] == 4:
                        match_stats[str(drag_df['DragElement'][2])+'Soul'] = side #team with soul
            #calculate dragon differences by each type of dragon
            for drag_elem in list(drag_df['DragElement'].unique()):
                match_stats[str(drag_elem)+'diff'] = drag_df.query('DragElement == @drag_elem and team == "blue"').shape[0] - drag_df.query('DragElement == @drag_elem and team == "red"').shape[0]
    return match_stats

def create_obj_list(timeline):
    '''
    Create a pandas dataframe of neutral objectives taken in the match timeline given.
    OUTPUT df: monsterType, DragElement, team that captured objective (red or blue)
    '''
    match_obj = []
    for i in range(len(timeline)):
        for event in timeline[i]['events']:
            if event['type'] == 'ELITE_MONSTER_KILL':
                if event['killerId'] == 0:
                    pass
                elif event['killerId'] > 0:
                    obj = {}
                    obj['ObjectiveType'] = event['monsterType']
                    if event['monsterType'] == 'DRAGON':
                        obj['DragElement'] = event['monsterSubType']
                    obj['timestamp'] = event['timestamp']
                    if 1<= event['killerId'] <= 5:
                        obj['team'] = 'blue'
                    elif 6<= event['killerId'] <= 10:
                        obj['team'] = 'red'
                    match_obj.append(obj)
    return match_obj
                    
def extract_matchstate_atm(gameId, time):
    '''
    Extract information of captured neutral objectives at 5 minute timeframes intervals 
    and save it preinitialized global dicts. 
    Individual dicts represent each time interval.
    Extracted parameters:
    - Dragons: difference between teams in number of dragons killed for each type of dragon (infernal, ocean, mountain, cloud, elder)
    - type of Dragon soul and the team that captured it
    - Rift herald and baron - difference in numbers of objectives killed between teams
    '''
    match_stats = {} #initialize dict for match
    #create a key for objective stats
    match_obj = create_obj_list(match_timeline_dict[gameId]['frames'][:time])

    if len(match_obj) > 0:
        obj_timeline_df = pd.DataFrame(match_obj)

        if obj_timeline_df[obj_timeline_df['ObjectiveType'] == 'DRAGON'].shape[0] > 0:

            #store team+timestamp of any elder dragons
            drag_df = obj_timeline_df[obj_timeline_df['ObjectiveType'] == 'DRAGON'].reset_index() #slice df of dragons only

            for side in ['blue', 'red']: #does either side have soul
                if drag_df.query('DragElement != "ELDER_DRAGON" and team == @side').shape[0] == 4:
                    match_stats[str(drag_df['DragElement'][2])+'Soulteam'] = side #team with soul
            for drag_elem in list(drag_df['DragElement'].unique()):
                match_stats[str(drag_elem)+'diff'] = drag_df.query('DragElement == @drag_elem and team == "blue"').shape[0] - drag_df.query('DragElement == @drag_elem and team == "red"').shape[0]

            #for row_idx, row in elem_drag_df.iterrows():
                #match_stats[str(row_idx+1)+str(row['DragElement'])+'team'] = row['team']

        if obj_timeline_df[obj_timeline_df['ObjectiveType'] != 'DRAGON'].shape[0] > 0:
            #store details about rift heralds and barons kill diff
            for obj_type in ['RIFTHERALD', 'BARON_NASHOR']:

                #slice the df with the relevant objective
                obj_type_df = obj_timeline_df[obj_timeline_df['ObjectiveType'] == obj_type].reset_index()
                #for each herald/baron, extract the team that killed the objective and the time it occured
                match_stats[str(obj_type)+'diff'] = obj_type_df[obj_type_df['team'] == 'blue'].shape[0] - obj_type_df[obj_type_df['team'] == 'red'].shape[0]
        return match_stats

def ini_time_dicts(max_time=60, start_min=10, interval_min=5):
    '''
    initialize dicts for saving gamestates at different time intervals
since the longest game is under 59 minutes, 60 minutes will be used as the max time interval
    '''
    list_time_dicts = {}
    t = 10
    while t in range(0, max_time):
        list_time_dicts[t] = {}
        t+=5

def gamestate_by_time(matches):
    '''
    Obtain post-game match stats and at different time intervals 
    saved as two different dicts with the match ID's as keys.
    
    '''
    match_results_dict = {}
    list_time_dicts = ini_time_dicts()

    for gameId in matches:
        if gameId in match_timeline_dict.keys():
            match_results = extract_match_results(gameId)
            match_results_dict [gameId] = match_results
            
            match_by_time = {}
            match_duration = int(match_detail_dict[gameId]['gameDuration']/60)
            t = 10
            while t <= match_duration:
                list_time_dicts[t][gameId] = extract_matchstate_atm(gameId, t)
                list_time_dicts[t][gameId]['Winner'] = match_results['Winner']
                t+=5
        #match_by_time_dict [gameId] = match_by_time
    
        match_results = extract_match_results(gameId)
        match_results_dict [gameId] = match_results
        
        
    return match_results_dict, list_time_dicts

def count_dictvals_above_thres(dict_vals, thres=0):
    '''
    Returns the number of dict vals in a dictionary 
    that's above a defined length threshold
    '''
    n = 0
    for val in dict_vals:
        if len(val) > thres:
            n+=1
    return n
