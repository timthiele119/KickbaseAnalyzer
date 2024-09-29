import sys, os

gitrepo = '/Users/Tim/Documents/KickbaseAnalyzer/KickbaseAnalyzerPowerBI'
if gitrepo not in sys.path:
    sys.path.append(gitrepo)
os.chdir(gitrepo)

from src.DataPipeline import DataPipeline

pipe = DataPipeline()

market_player_df = DataPipeline().fetch_market_data()
top_25_player_df = DataPipeline().fetch_top25_data()