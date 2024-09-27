import os, sys
from dotenv import load_dotenv
from API.Kickbase import KickbaseHandler
from API.OpenDB import OpenDBHandler


class DataPipeline:
    
    def __init__(self):
        pass
    
    def fetch_market_data(self):
        players = KickbaseHandler().load_players_on_market()
        market_player_df = KickbaseHandler().transform_to_player_df(players)
        print(market_player_df)
        
        # for each fetched player, fetch team match plan
        OpenDBHandler().get_matches_by_team(teamFilterstring="Borussia Dortmund")
        
        # construct measure then to create recommendation
        
        # save it in excel sheet and show it PowerBI
        
        
if __name__ == "__main__":
    DataPipeline().fetch_market_data()