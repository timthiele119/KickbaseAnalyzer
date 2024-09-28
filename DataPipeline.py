import os, sys
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from API.Kickbase import KickbaseHandler
from API.OpenDB import OpenDBHandler
from utils.helper import load_team_name_mapping_json


class DataPipeline:
    
    def __init__(self):
        self.team_id_to_name_mapping = load_team_name_mapping_json()
    
    def fetch_market_data(self):
        players = KickbaseHandler().load_players_on_market()
        market_player_df = KickbaseHandler().transform_to_player_df(players)
        
        # Construct measure from OpenDB data source and join it
        market_player_df["Table Coeff."] = np.nan
        market_player_df["Point Coeff."] = np.nan
        market_player_df["Club Measure"] = np.nan
        for team_name in self.team_id_to_name_mapping.values(): 
            table_df = OpenDBHandler().get_bl_league_table()
            match_df = OpenDBHandler().get_matches_by_team(teamFilterstring=team_name)
            table_coeff, point_coeff, club_measure = OpenDBHandler().get_measure_coeff(
                        team_name, table_df, match_df
                    )
            market_player_df.loc[market_player_df["Team Name"] == team_name, "Table Coeff."] = table_coeff
            market_player_df.loc[market_player_df["Team Name"] == team_name, "Point Coeff."] = point_coeff
            market_player_df.loc[market_player_df["Team Name"] == team_name, "Club Measure"] = club_measure
        
        market_player_df.to_csv("market_player_df.csv")


if __name__ == "__main__":
    DataPipeline().fetch_market_data()