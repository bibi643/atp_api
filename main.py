# Libraries

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
from datetime import datetime, date
import operator

from functions import import_data, tournament_db, players_db

######################################################################################################
file= 'atp_data.csv'
data_raw= import_data(file)

api = FastAPI(title='ATP API with main types of routes',
              description= 'API with main routes',
              openapi_tags=[
                  {'name': 'Tournaments',
                   'description': 'Routes for the Tournaments'
                  },
                  {'name':'Players',
                   'description':'Routes for the Players'
                   }
              ])

class Tournaments (BaseModel):
    Tournament: str
    Location: str
    Series: str
    Court: str
    Surface: str
    Best_of: int
    def __getitem__(self, item):
        return getattr(self, item)




    





##########################################################################################################

# Routes

tournament_df_dict= tournament_db(data_raw)
player_db_current_dict = players_db(data_raw)

@api.get('/tournaments',tags=['Tournaments'])
def get_tournaments_db():
    '''Function to use the tournament db. Return a list of dicitionnaries
    '''
    return tournament_df_dict



@api.get('/players',tags=['Players'])
def get_players_db():
    '''Get the last data for each player of the data base
    Uses the data frame raw and isolate the datas from the player to return a  list of dictionnaries.
    '''
    
    return player_db_current_dict





class Players (BaseModel):
    Player: str
    Date: date
    Rank: int
    elo: float = 1500.00
    def __getitem__(self, item):
        return getattr(self, item)

@api.post('/add_new_player',tags=['Players'])
def post_new_player(player: Players):
    player_db_current_dict =get_players_db()
    player.Player = player.Player.upper()

    player_db_current_dict.append(player)
    player_db_current_dict= sorted(player_db_current_dict, key = operator.itemgetter('Player'))
    
   
    
    return player_db_current_dict



@api.put('/add_new_player',tags=['Players'])
def put_new_player(player: Players):
    player_db_current_dict =get_players_db()
    player.Player = player.Player.upper()

    player_db_current_dict.append(player)
    player_db_current_dict= sorted(player_db_current_dict, key = operator.itemgetter('Player'))
    
    
    
    return player_db_current_dict



@api.delete('/delete_player',tags=['Players'])
def delete_player(player_to_delete: str):
    player_db_current_dict =get_players_db()

    player_to_delete= player_to_delete.upper()
    player_db_current_dict = list(filter(lambda i: i['Player'] != player_to_delete, player_db_current_dict))
    return player_db_current_dict

# Routes for tournamennts

@api.post('/add_new_tournament',tags=['Tournaments'])
def post_new_tournament(tournament: Tournaments):
    tournament_df_dict =get_tournaments_db()
    tournament.Tournament= tournament.Tournament.upper()
    #tournament = dict(tournament)
    tournament_df_dict.append(tournament)
    tournament_df_dict= sorted(tournament_df_dict, key = operator.itemgetter('Tournament'))
    
   
    
    return tournament_df_dict



@api.put('/add_new_tournament',tags=['Tournaments'])
def put_new_tournament(tournament: Tournaments):
    tournament_df_dict =get_tournaments_db()
    tournament.Tournament= tournament.Tournament.upper()
    #tournament = dict(tournament)
    tournament_df_dict.append(tournament)
    tournament_df_dict= sorted(tournament_df_dict, key = operator.itemgetter('Tournament'))
    
   
    
    return tournament_df_dict







@api.delete('/delete_tournament',tags=['Tournaments'])
def delete_tournament(tournament_to_delete: str):
    tournament_df_dict= get_tournaments_db()

    tournament_to_delete= tournament_to_delete.upper()
    tournament_df_dict= list(filter(lambda i: i['Tournament'] != tournament_to_delete, tournament_df_dict))
    return tournament_df_dict