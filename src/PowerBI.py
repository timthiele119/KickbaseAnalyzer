# Paste this in PowerBI

import sys, os

gitrepo = '/Users/Tim/Documents/KickbaseAnalyzer/KickbaseAnalyzerPowerBI'
wdir = os.path.join(gitrepo, 'src')

if gitrepo not in sys.path:
    sys.path.append(gitrepo)
    sys.path.append(wdir)

os.chdir(gitrepo)

from src.DataPipeline import DataPipeline

pipe = DataPipeline()

market_player_df = DataPipeline().fetch_market_data()
top_25_player_df = DataPipeline().fetch_top25_data()