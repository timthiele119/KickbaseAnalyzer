import os, sys
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from API.Kickbase import KickbaseHandler
from API.OpenDB import OpenDBHandler
from utils.helper import load_team_name_mapping_json, exception_handler

# switch CURRENT_MATCHDAY on friday evenings at 20:30
CURRENT_MATCHDAY = 5

class DataPipeline:
    
    def __init__(self):
        self.team_id_to_name_mapping = load_team_name_mapping_json()
    
    @exception_handler
    def fetch_market_data(self):
        kb_handler = KickbaseHandler()
        db_handler = OpenDBHandler()
        
        players = kb_handler.load_players_on_market()
        market_player_df = kb_handler.transform_to_player_df(players)
        
        for team in market_player_df["Team Name"].unique().tolist():
            table_df = db_handler.get_bl_league_table()
            match_df = db_handler.get_matches_by_team(teamFilterstring=team)
            enriched_match_df = db_handler.enrich_match_df_by_measures(table_df, match_df, current_matchday=CURRENT_MATCHDAY)
            
            columns_to_add = ["static_req_table_coeff", "req_point_coeff", "static_opp_table_coeff", "opp_point_coeff"]
            if not enriched_match_df.empty and CURRENT_MATCHDAY - 1 in enriched_match_df.index:
                enriched_match_df = enriched_match_df.loc[CURRENT_MATCHDAY - 1]
                enriched_match_df = pd.DataFrame(enriched_match_df).T
                for column in columns_to_add:
                    team_mask = market_player_df["Team Name"] == enriched_match_df["requested_team"].values[0]
                    market_player_df.loc[team_mask, column] = enriched_match_df[column].values[0]
                    
            print(f"Completed merging for team: {team}")

        market_player_df.to_csv("market_player_df.csv")


if __name__ == "__main__":
    DataPipeline().fetch_market_data()