# Hobby Project: Kickbase Analyzer

## ⚽️ Kickbase
Kickbase is a football manager app that allows users to create and manage their own football teams based on real-time performance data from actual football matches. 
The app offers live statistics provided by Opta Sports. Users can buy, sell, and trade players, track live scores, and compete in leagues with friends. Link: https://www.kickbase.com/de.

## 🎯 Project Overview
This repository contains code to request data from a personal Kickbase account and to further provide it downstream for data analytics using PowerBI, 
enabling making data-driven and intelligent decisions for the next matchday.
It enriches the retrieved information about players with additional information about the league and club of the players fetched from OpenDB; 
to e.g. support buying and lineup decisions.
Unfortunately, I have no business account of Microsoft, so I cannot share the PowerBI visualizations as webapp online. However, find the attached PowerBI file and the visualizations of the current dashboards as PDF under directory `\PowerBI`.

## ✨ Features
- Possibility to fetch data about one owns lineup, the market in the league, the top 25 players in the game
- Player data from kickbase can be enriched with metrics such as the clubs league table position, the current form and the next matchups using OpenDB
- Data can be provided as DataFrames using the Python script `\src\PowerBI.py` or as CSV-Files
- Data gets visualized in using PowerBI, having evaluations for current market players, top 25 players and the respective teams

## 🌱 Why I Built This
This project was driven by my interest in data analytics, my engagement to learn more about PowerBI (a I build this project for delivering the data to it) 
and my recent decision to start playing Kickbase in the Bundesliga 2024/2025 Season.

## 🛠️ Technologies Used
- **Programming Language(s):** Python
- **Libraries/Frameworks:** Pandas, NumPy
- **Tools/IDE:** VSCode, Git, PowerBI

## 📦 Installation and Setup
1. Clone the repository:
    ```bash
    git clone git@github.com:timthiele119/KickbaseAnalyzerPowerBI.git
    ```
2. Create a virtual environment and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Create an .env-file as with the following example information:
    ```
    CURRENT_MATCHDAY = 1
    KICKBASE_USERNAME = "KickbaseUser123"
    KICKBASE_PASSWORD = "Password123"
    KICKBASE_LEAGUE_TO_USE = "KickbaseLeague123"
    ```
4. Run the project for an example demonstration of the datapipeline (saves player dataframe as csv in dir):
    ```
    python src\DataPipeline.py
    ```
5. Run the code of the following file in PowerBI (using Python to retrieve data)
    ```
    src\PowerBI.py
    ```

5. For using it as datapipeline in PowerBI, open the file "". Paste the script "" as Python Code in the data load option in PowerBI.

## 👨🏽‍💻 Resources
- Kickbase Python API:        https://github.com/kevinskyba/kickbase-api-python
- Kickbase Python API Doc:    https://kevinskyba.github.io/kickbase-api-python/index.html
- OpenLigaDB:                 https://www.openligadb.de
- OpenLigaDB Swagger Doc:     https://api.openligadb.de/index.html

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.