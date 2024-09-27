import requests

# Define your parameters
league_shortcut = "bl1"  # Replace with your league shortcut
league_season = 2024      # Replace with your league season
group_order_id = 4        # Replace with your group order ID

# Construct the API URL
api_url = f"https://api.openligadb.de/getmatchdata/{league_shortcut}/{league_season}/{group_order_id}"

# Send a GET request to fetch data from the API
response = requests.get(api_url)

# GET MATCHDAY DATA

# Check if the request was successful
if response.status_code == 200:
    match_data = response.json()  # Convert the response to JSON
    for match in match_data:
        # Safely access team names
        team1_name = match['team1']['teamName'] if match.get('team1') else 'Unknown Team 1'
        team2_name = match['team2']['teamName'] if match.get('team2') else 'Unknown Team 2'
        
        # Safely access location information
        location_city = match['location']['locationCity'] if match.get('location') else 'Unknown Location'
        
        # Safely access match date and time
        match_time = match['matchDateTime'] if 'matchDateTime' in match else 'Unknown Time'

        # Print match information
        print(f"Matchup: {team1_name} - {team2_name}, Location: {location_city}, Time: {match_time}")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    
    
# GET
# Construct the API URL
api_url = f"https://api.openligadb.de/getbltable/{league_shortcut}/{league_season}"
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    table_data = response.json()
    
    # Loop through each team in the table data
    i = 0
    for team in table_data:
        i += 1
        # Extract relevant information
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

        # Print out the information for each team
        print(f"Position: {team_info['position']}")
        print(f"Team: {team_info['teamName']}")
        print(f"Points: {team_info['points']}, Matches: {team_info['matches']}, Won: {team_info['won']}, Lost: {team_info['lost']}, Draw: {team_info['draw']}")
        print(f"Goals: {team_info['goals']}, Opponent Goals: {team_info['opponentGoals']}, Goal Difference: {team_info['goalDiff']}")
        print(f"Team Icon URL: {team_info['teamIconUrl']}\n")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")