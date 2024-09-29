import sys

gitrepo = '/c/Users/Tim/Documents/KickbaseAnalyzer/KickbaseAnalyzerPowerBI'
if gitrepo not in sys.path:
    sys.path.append(gitrepo)

from DataPipeline import DataPipeline

pipe = DataPipeline()

market_player_df = DataPipeline().fetch_market_data()
top_25_player_df = DataPipeline().fetch_top25_data()