import os, sys
from dotenv import load_dotenv
import json
import pandas as pd

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
kickbase_api_path = os.path.join(base_dir, 'kickbase-api-python')
sys.path.append(kickbase_api_path)

wdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(wdir)

from kickbase_api.kickbase import Kickbase
from utils.helper import exception_handler


class KickbaseHandler:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv('KICKBASE_USERNAME')  
        self.password = os.getenv('KICKBASE_PASSWORD')
        self.league_to_use_name = os.getenv('KICKBASE_LEAGUE_TO_USE')
        self.league_to_use = None
        
        self.login()
        self.get_league()
        self.load_team_name_mapping_json()
    
    @exception_handler
    def login(self):
        self.kickbase = Kickbase()
        self.user, self.leagues = self.kickbase.login(self.username, self.password)
        print(f"Kickbase login successful.\n")
        
    @exception_handler
    def get_league(self):
        self.league_to_use = None
        for league in self.leagues:
            if league.name == self.league_to_use_name:
                self.league_to_use = league
        print(f"League selected: {self.league_to_use_name}\n")
    
    @exception_handler
    def load_team_name_mapping_json(self):
        with open('teamIDtoNameMapping.json', 'r') as json_file:
            self.team_id_to_name_mapping = json.load(json_file)
        print("Team name mapping loaded successfully.\n")
    
    def set_player_info(self, player):
        return {
            "First Name": player.first_name,
            "Last Name": player.last_name,
            "Team ID": player.team_id,
            "Team Name": self.team_id_to_name_mapping[player.team_id],
            "Position": player.position,
            "Total Points": player.totalPoints,
            "Average Points": player.average_points,
            "Market Value": player.market_value,
            "Market Value Trend": player.market_value_trend,
            "Profile Path": player.profile_path,
            "Profile Big Path": player.profile_big_path,
        }
                
    def print_player_info(self, player):
        print(self.set_player_info(player), "\n\n")
    
    def transform_to_player_df(self, players):
        player_data = []
        for player in players:
            player_data.append(self.set_player_info(player))
        player_df = pd.DataFrame(player_data)
        return player_df
    
    @exception_handler
    def load_top_25_players(self):
        top_25_players = self.kickbase.top_25_players()
        for player in top_25_players:
            self.set_player_info(player)
        print(f"Loading top 25 players was successful.\n")
        return top_25_players
        
    @exception_handler
    def load_players_on_market(self):
        market = self.kickbase.market(self.league_to_use)
        for player in market.players:
            self.set_player_info(player)
        print(f"Loading players on the market was successful.\n")
        return market.players
    
    @exception_handler
    def load_players_from_team(self, team_id: str = '3'):
        team_players = self.kickbase.team_players(team_id)
        for player in team_players:
            self.set_player_info(player)
        print(f"Loading players from the team with id {team_id} was successful.\n")
        return team_players
    
    @exception_handler
    def load_own_lineup(self):
        lineup_players = self.kickbase.line_up(self.league_to_use)
        for player in lineup_players:
            self.set_player_info(player)
        print(f"Loading players from the own lineup was successful.\n")
        return lineup_players
            

if __name__ == "__main__":
    players = KickbaseHandler().load_top_25_players()
    top_25_player_df = KickbaseHandler().transform_to_player_df(players)
    
    players = KickbaseHandler().load_players_on_market()
    market_player_df = KickbaseHandler().transform_to_player_df(players)