# Libraries

import pandas as pd
from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel








# Functions for get routes


file= 'atp_data.csv'
def import_data(file):
    data_raw = pd.read_csv(file)
    return data_raw


def tournament_db(data_raw):
    '''Uses the data raw and isolate the data from each tournament, and return a dictionnary.
    '''
    tournament_df= data_raw[['Location', 'Tournament', 'Series', 'Court', 'Surface', 'Best of']]
    tournament_df = tournament_df.rename(columns = {'Best of': 'Best_of'})
    tournament_df = tournament_df.groupby('Tournament').first().reset_index()
    tournament_df['Tournament']= tournament_df['Tournament'].str.upper()
    tournament_df['Tournament'] = tournament_df['Tournament'].str.strip()
    tournament_df_dict = tournament_df.to_dict('records')
    return tournament_df_dict


def players_db(data_raw):
    '''Get the last data for each player of the data base
    Uses the data frame raw and isolate the datas from the player to return a dictionnary.
    '''
     
    df_player = data_raw[['Date','Winner', 'Loser','WRank','LRank','elo_winner','elo_loser']]

    #extract winner and loser
    player_list1 = df_player [['Date', 'Winner', 'WRank','elo_winner']]
    player_list2 = df_player [['Date','Loser','LRank','elo_loser']]

    #Rename the columns for further concatenation
    player_list1 = player_list1.rename(columns={"Winner": "Player", "WRank": "Rank", 'elo_winner':'elo'})
    player_list2 = player_list2.rename(columns={"Loser": "Player", "LRank": "Rank", 'elo_loser':'elo'})

    #remove any heading and tailing space in player name
    player_list1['Player']= player_list1['Player'].str.strip()
    player_list2['Player']= player_list2['Player'].str.strip()

    player_db = pd.DataFrame(columns=['Date','Player','Rank','elo'])

    player_db_full= pd.concat([player_db,player_list1,player_list2])
    player_db_full['Player'] = player_db_full['Player'].str.upper()

    player_db_full = player_db_full.sort_values(['Player','Date']).reset_index(drop=True)


    player_db_current = player_db_full.groupby('Player').last().reset_index()
   
    player_db_current_dict = player_db_current.to_dict('records')


    return player_db_current_dict



############################################################################################





    
    






# Fonctions for put routes







# Fonctions for post routes







# Fonctions for delete routes