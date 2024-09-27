import os, sys
from dotenv import load_dotenv
from API.Kickbase import KickbaseHandler
from API.OpenDB import OpenDBHandler


class DataPipeline:
    
    def __init__(self):
        
    
    def fetch_data(self):
        KickbaseHandler().load_players_on_market()