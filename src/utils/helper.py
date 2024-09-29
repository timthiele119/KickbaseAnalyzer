import functools
import json
import os, sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            print(f"Exception in method '{func.__name__}': {e}")
    return wrapper


def load_team_name_mapping_json():
    with open('teamIDtoNameMapping.json', 'r') as json_file:
        team_id_to_name_mapping = json.load(json_file)
    return team_id_to_name_mapping


def load_team_name_mapping_py():
    import teamIDtoNameMapping.map_
    return map_