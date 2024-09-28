import json
import os, sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

def load_team_name_mapping_json():
    with open('teamIDtoNameMapping.json', 'r') as json_file:
        team_id_to_name_mapping = json.load(json_file)
    return team_id_to_name_mapping