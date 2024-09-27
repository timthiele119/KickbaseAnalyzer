import requests
import json
import pandas as pd

class OpenDBHandler:
    def __init__(self):
        self.base_url = f"https://api.openligadb.de"
        self.load_team_name_mapping_json()
    
    def load_team_name_mapping_json(self):
        with open('teamIDtoNameMapping.json', 'r') as json_file:
            self.team_id_to_name_mapping = json.load(json_file)

    def get_matchups(
        self, 
        league_shortcut: str = "bl1", 
        league_season: str = "2024", 
        matchday_number: str = "1",
    ):
        url = self.base_url + f"/getmatchdata/{league_shortcut}/{league_season}/{matchday_number}"
        response = requests.get(url)
        
        if response.status_code == 200:
            match_data = response.json()
            for match in match_data:
                team1_name = match['team1']['teamName'] if match.get('team1') else 'Unknown Team 1'
                team2_name = match['team2']['teamName'] if match.get('team2') else 'Unknown Team 2'
                location_city = match['location']['locationCity'] if match.get('location') else 'Unknown Location'
                match_time = match['matchDateTime'] if 'matchDateTime' in match else 'Unknown Time'

                match_info = {
                    "team1": team1_name,
                    "team2": team2_name,
                    "location": location_city,
                    "time": match_time
                }
                print(match_info)
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    
    def get_matches_by_team(
        self,
        teamFilterstring: str,
        weekCountPast: int = 5,
        weekCountFuture: int = 5
    ):
        url = self.base_url + f"/getmatchesbyteam/{teamFilterstring}/{weekCountPast}/{weekCountFuture}"
        response = requests.get(url)
        
        if response.status_code == 200:
            match_data = response.json()
            matches = []
            for match in match_data:
                if not "1. Fußball-Bundesliga" in match["leagueName"]:
                    continue
                
                match_info = {}
                match_info["requested_team"] = teamFilterstring
                match_info["home_team"] = match['team1']['teamName'] if match.get('team1') else 'Unknown Team 1'
                match_info["away_team"] = match['team2']['teamName'] if match.get('team2') else 'Unknown Team 2'
                match_info["datetime"] = match['matchDateTime'] if 'matchDateTime' in match else 'Unknown Time'
                match_info["matchIsFinished"] = match["matchIsFinished"]
                
                if match_info["matchIsFinished"]:
                    for result in match["matchResults"]:
                        if result["resultName"] == "Endergebnis":
                            match_info["home_team_goals"] = result['pointsTeam1']
                            match_info["away_team_goals"] = result['pointsTeam2']
                            
                            if teamFilterstring == match_info["home_team"]:
                                match_info["requested_team_goals"] = match_info["home_team_goals"]
                            else:
                                match_info["requested_team_goals"] = match_info["away_team_goals"]
                            
                            goal_diff = match_info["home_team_goals"] - match_info["away_team_goals"]
                            if goal_diff > 0:
                                match_info["home_team_points"] = 3
                                match_info["away_team_points"] = 0
                            elif goal_diff == 0:
                                match_info["home_team_points"] = match_info["away_team_points"] = 1
                            else:
                                match_info["home_team_points"] = 0
                                match_info["away_team_points"] = 3
                                
                            if teamFilterstring == match_info["home_team"]:
                                match_info["requested_team_points"] = match_info["home_team_points"]
                            else:
                                match_info["requested_team_points"] = match_info["away_team_points"]
                            
                matches.append(match_info)
            
            match_df = pd.DataFrame(matches).drop_duplicates()
            return match_df
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    def get_bl_league_table(
        self,
        league_shortcut: str = "bl1",
        league_season: str = "2024",
    ):
        url = self.base_url + f"/getbltable/{league_shortcut}/{league_season}"
        response = requests.get(url)
        
        if response.status_code == 200:
            table_data = response.json()
            i = 0
            table_list = []
            for team in table_data:
                i += 1
                team_info = {
                    "position": i,
                    "teamName": team.get("teamName"),
                    "shortName": team.get("shortName"),
                    "points": team.get("points"),
                    "matches": team.get("matches"),
                    "won": team.get("won"),
                    "lost": team.get("lost"),
                    "draw": team.get("draw"),
                    "goals": team.get("goals"),
                    "opponentGoals": team.get("opponentGoals"),
                    "goalDiff": team.get("goalDiff"),
                    "teamIconUrl": team.get("teamIconUrl")
                }
                table_list.append(team_info)
            table_df = pd.DataFrame(table_list)
            return table_df
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    def get_measure(self, requested_team, table_df, match_df):
        table_position = table_df[table_df["teamName"] == requested_team]["position"].values[0]
        point_history = match_df["requested_team_points"].fillna(value=0).sum()
        # goal_diff_history = match_df["requested_team_goals"].fillna(value=0).sum()
        table_coeff = (18 - table_position) / (18 - 1)
        point_coeff = (point_history - 0)/(15 - 0)
        club_measure = 0.5 * table_coeff +  0.5 * point_coeff
        print(f"Team: {requested_team}")
        print(f"Table Position: {table_position}")
        print(f"Point History: {point_history}")
        print(f"table_coeff: {table_coeff}, point_coeff: {point_coeff}")
        print(f"Club Measure: {club_measure}")
        return club_measure
        
if __name__ == "__main__":
    requested_team="FC Bayern München"
    table_df = OpenDBHandler().get_bl_league_table()
    match_df = OpenDBHandler().get_matches_by_team(teamFilterstring=requested_team)
    OpenDBHandler().get_measure(requested_team, table_df, match_df)