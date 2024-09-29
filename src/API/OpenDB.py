import sys, os
import requests
import pandas as pd

wdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(wdir)
from utils.helper import exception_handler

class OpenDBHandler:
    def __init__(self):
        self.base_url = f"https://api.openligadb.de"

    @exception_handler
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
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    
    @exception_handler
    def get_matches_by_team(
        self,
        teamFilterstring: str,
        weekCountPast: int = 5,
        weekCountFuture: int = 5,
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
                match_info["opponent_team"] = match_info["home_team"] if teamFilterstring == match_info["away_team"] else match_info["away_team"]
                match_info["datetime"] = match['matchDateTime'] if 'matchDateTime' in match else 'Unknown Time'
                match_info["matchIsFinished"] = match["matchIsFinished"]
                
                if match_info["matchIsFinished"]:
                    for result in match["matchResults"]:
                        if result["resultName"] == "Endergebnis":
                            if teamFilterstring == match_info["home_team"]:
                                match_info["requested_team_goals"] = result['pointsTeam1']
                                match_info["opponent_team_goals"] = result['pointsTeam2']
                            else:
                                match_info["requested_team_goals"] = result['pointsTeam2']
                                match_info["opponent_team_goals"] = result['pointsTeam1']
                            
                            goal_diff = match_info["requested_team_goals"] - match_info["opponent_team_goals"]
                            if goal_diff > 0:
                                match_info["requested_team_points"] = 3
                                match_info["opponent_team_points"] = 0
                            elif goal_diff == 0:
                                match_info["requested_team_points"] = match_info["opponent_team_points"] = 1
                            else:
                                match_info["requested_team_points"] = 0
                                match_info["opponent_team_points"] = 3
                            
                matches.append(match_info)
            
            match_df = pd.DataFrame(matches).drop_duplicates()
            return match_df
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    @exception_handler
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
    
    @exception_handler
    def get_measure_coeff(self, table_df, match_df, requested_team, matchday_to_compute_for: int):
        table_position = table_df[table_df["teamName"] == requested_team]["position"].values[0]
        point_history = match_df["requested_team_points"].fillna(value=0).sum()
        table_coeff = (18 - table_position) / (18 - 1)
        point_coeff = (point_history - 0)/(matchday_to_compute_for * 3 - 0)
        return table_coeff, point_coeff
    
    @exception_handler
    def enrich_match_df_by_measures(self, table_df, match_df, current_matchday):
        """
        Enrich match_df with calculated coefficients for each team's form and table performance.
        """ 
        def _calculate_team_coeffs(team, comp_matchday, idx):
            """
            Helper function to calculate table and point coefficients for a team.
            """
            team_match_df = OpenDBHandler().get_matches_by_team(
                teamFilterstring=team, 
                weekCountPast=current_matchday,
                weekCountFuture=0
            )
            team_match_df = team_match_df.loc[:idx-1]

            if comp_matchday == 1:
                print(f"No previous matches available for {team}, setting coeffs to 0.5.")
                return 0.5, 0.5

            return OpenDBHandler().get_measure_coeff(table_df, team_match_df, team, comp_matchday - 1)

        for idx in match_df.index:
            comp_matchday = idx + 1
            requested_team = match_df.loc[idx, "requested_team"]
            opponent_team = match_df.loc[idx, "opponent_team"]

            req_table_coeff, req_point_coeff = _calculate_team_coeffs(requested_team, comp_matchday, idx)
            match_df.loc[match_df["requested_team"] == requested_team, "static_req_table_coeff"] = req_table_coeff
            match_df.loc[match_df["requested_team"] == requested_team, "req_point_coeff"] = req_point_coeff

            opp_table_coeff, opp_point_coeff = _calculate_team_coeffs(opponent_team, comp_matchday, idx)
            match_df.loc[match_df["opponent_team"] == opponent_team, "static_opp_table_coeff"] = opp_table_coeff
            match_df.loc[match_df["opponent_team"] == opponent_team, "opp_point_coeff"] = opp_point_coeff

        return match_df


if __name__ == "__main__":
    # Example usage
    requested_team="FC Bayern München"
    table_df = OpenDBHandler().get_bl_league_table()
    match_df = OpenDBHandler().get_matches_by_team(teamFilterstring=requested_team)
    enriched_match_df = OpenDBHandler().enrich_match_df_by_measures(table_df, match_df, current_matchday=5)
    print(enriched_match_df)