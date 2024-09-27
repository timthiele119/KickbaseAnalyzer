import requests

class OpenDBHandler:
    def __init__(self):
        self.base_url = f"https://api.openligadb.de"
              
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

    def get_bl_league_table(
        self,
        league_shortcut: str = "bl1",
        league_season: str = "2023",
    ):
        url = self.base_url + f"/getbltable/{league_shortcut}/{league_season}"
        response = requests.get(url)
        
        if response.status_code == 200:
            table_data = response.json()
            i = 0
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
                print(f"Position: {team_info['position']}")
                print(f"Team: {team_info['teamName']}")
                print(f"Points: {team_info['points']}, Matches: {team_info['matches']}, Won: {team_info['won']}, Lost: {team_info['lost']}, Draw: {team_info['draw']}")
                print(f"Goals: {team_info['goals']}, Opponent Goals: {team_info['opponentGoals']}, Goal Difference: {team_info['goalDiff']}")
                print(f"Team Icon URL: {team_info['teamIconUrl']}\n")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
            
if __name__ == "__main__":
    OpenDBHandler().get_bl_league_table()
    OpenDBHandler().get_matchups(matchday_number="5")