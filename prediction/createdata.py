import math
import random
import time
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from sklearn.model_selection import train_test_split
from sklearn import svm

all_season_data = pd.read_csv('/Users/isalyubimova/ballinsights/data_prep/MRegularSeasonDetailedResults.csv')

day_zero_data = pd.read_csv('/Users/isalyubimova/ballinsights/data_prep/MSeasons.csv')
day_zero = day_zero_data['DayZero']
day_zero = pd.to_datetime(day_zero)
time_data = all_season_data[['Season', 'DayNum']].copy()
time_data['DayZero'] = day_zero
make_new_dates = []

# FIX DATA DATES

for index, row in time_data.iterrows():
    if row['Season'] == 2003:
        make_new_dates.append('2002-11-04')
    if row['Season'] == 2004:
        make_new_dates.append('2003-11-03')
    if row['Season'] == 2005:
        make_new_dates.append('2004-11-01')
    if row['Season'] == 2006:
        make_new_dates.append('2005-10-31')
    if row['Season'] == 2007:
        make_new_dates.append('2006-10-30')
    if row['Season'] == 2008:
        make_new_dates.append('2007-11-05')
    if row['Season'] == 2009:
        make_new_dates.append('2008-11-03')
    if row['Season'] == 2010:
        make_new_dates.append('2009-11-02')
    if row['Season'] == 2011:
        make_new_dates.append('2010-11-01')
    if row['Season'] == 2012:
        make_new_dates.append('2011-10-31')
    if row['Season'] == 2013:
        make_new_dates.append('2012-11-05')
    if row['Season'] == 2014:
        make_new_dates.append('2013-11-04')
    if row['Season'] == 2015:
        make_new_dates.append('2014-11-03')
    if row['Season'] == 2016:
        make_new_dates.append('2015-11-02')
    if row['Season'] == 2017:
        make_new_dates.append('2016-10-31')
    if row['Season'] == 2018:
        make_new_dates.append('2017-10-30')
    if row['Season'] == 2019:
        make_new_dates.append('2018-11-05')
    if row['Season'] == 2020:
        make_new_dates.append('2019-11-04')
    if row['Season'] == 2021:
        make_new_dates.append('2020-11-02')
    if row['Season'] == 2022:
        make_new_dates.append('2021-11-01')

time_data['DatePlayed'] = make_new_dates
time_data['DatePlayed'] = pd.to_datetime(time_data['DatePlayed'])

for index, row in time_data.iterrows():
    row['DatePlayed'] = row['DatePlayed'] + pd.Timedelta(days=row['DayNum'])

# FULLDATA refers to clean, usable data

fulldata = pd.concat([all_season_data[['WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc', 'WOR',
                                       'WDR', 'LOR', 'LDR', 'WBlk', 'LBlk']], time_data[['DatePlayed', 'Season']]], axis=1)
fulldata['WFGP'] = all_season_data['WFGM'] / all_season_data['WFGA']
fulldata['LFGP'] = all_season_data['LFGM'] / all_season_data['LFGA']

fulldata.sort_values(by='DatePlayed', inplace=True)
fulldata.reset_index(inplace=True, drop=True)

# ELO PROCESS HELPER FUNCTIONS

def win_probs(home_elo, away_elo, home_court_advantage):
    h = math.pow(10, home_elo / 400)
    r = math.pow(10, away_elo / 400)
    a = math.pow(10, home_court_advantage / 400)

    denom = r + a * h
    home_prob = a * h / denom
    away_prob = r / denom

    return home_prob, away_prob


def home_odds_on(home_elo, away_elo, home_court_advantage):
    h = math.pow(10, home_elo / 400)
    r = math.pow(10, away_elo / 400)
    a = math.pow(10, home_court_advantage / 400)
    return a * h / r


def update_elo(home_score, away_score, home_elo, away_elo, home_court_advantage):
    home_prob, away_prob = win_probs(home_elo, away_elo, home_court_advantage)

    if home_score - away_score > 0:
        home_win = 1
        away_win = 0
    else:
        home_win = 0
        away_win = 1

    # found to be optimal value
    k = 20

    updated_home_elo = home_elo + k * (home_win - home_prob)
    updated_away_elo = away_elo + k * (away_win - away_prob)

    return updated_home_elo, updated_away_elo

# ELO PROCEDURE CREATING NEW DATAFRAME

fulldata.sort_values(by='DatePlayed', inplace=True)
fulldata.reset_index(inplace=True, drop=True)
elo_df = pd.DataFrame(
    columns=['HomeTeam', 'AwayTeam', 'H_Team_Elo_Before', 'A_Team_Elo_Before', 'H_Team_Elo_After', 'A_Team_Elo_After'])
teams_elo_df = pd.DataFrame(columns=['Team', 'Elo', 'Date', 'Where_Played', 'Season'])

for index, row in fulldata.iterrows():
    print(index)
    if row['WLoc'] == 'H':
        home_team, away_team = row['WTeamID'], row['LTeamID']
    elif row['WLoc'] == 'A':
        home_team, away_team = row['LTeamID'], row['WTeamID']
    elif row['WLoc'] == 'N':
        rand = random.random()
        if rand < 0.5:
            home_team, away_team = row['WTeamID'], row['LTeamID']
        else:
            home_team, away_team = row['LTeamID'], row['WTeamID']
    where_played = row['WLoc']
    game_date = row['DatePlayed']
    season = row['Season']
    if row['WLoc'] == 'H':
        home_score, away_score = row['WScore'], row['LScore']
    elif row['WLoc'] == 'A':
        home_score, away_score = row['LScore'], row['WScore']
    elif row['WLoc'] == 'N':
        rand = random.random()
        if rand < 0.5:
            home_score, away_score = row['WScore'], row['LScore']
        else:
            home_score, away_score = row['LScore'], row['WScore']

    if home_team not in elo_df['HomeTeam'].values and home_team not in elo_df['AwayTeam'].values:
        h_team_elo_before = 1500
    # else:
        # h_team_elo_before = get_prev_elo(h_team, game_date, season, team_stats, elo_df)
    if away_team not in elo_df['HomeTeam'].values and away_team not in elo_df['AwayTeam'].values:
        a_team_elo_before = 1500
    # else:
        # a_team_elo_before = get_prev_elo(a_team, game_date, season, team_stats, elo_df)
    h_team_elo_after, a_team_elo_after = update_elo(home_score, away_score, h_team_elo_before, a_team_elo_before, 100)

    new_row = {'HomeTeam': home_team, 'AwayTeam': away_team, 'H_Team_Elo_Before': h_team_elo_before,
               'A_Team_Elo_Before': a_team_elo_before,
               'H_Team_Elo_After': h_team_elo_after, 'A_Team_Elo_After': a_team_elo_after}
    teams_row_one = {'Team': home_team, 'Elo': h_team_elo_before, 'Date': game_date,
                     'Where_Played': 'Home', 'Season': season}
    teams_row_two = {'Team': away_team, 'Elo': a_team_elo_before, 'Date': game_date,
                     'Where_Played': 'Away', 'Season': season}

    elo_df = elo_df.append(new_row, ignore_index=True)
    teams_elo_df = teams_elo_df.append(teams_row_one, ignore_index=True)
    teams_elo_df = teams_elo_df.append(teams_row_two, ignore_index=True)

elo_df.to_csv('elo_df.csv', index=False)

# For now, do not consider neutral games

elo_data = pd.read_csv('/Users/isalyubimova/ballinsights/elo_df.csv')
elo_data = elo_data[fulldata.WLoc != 'N']


fulldata = fulldata[fulldata.WLoc != 'N']
fulldata['HomeELO'] = elo_data['H_Team_Elo_After']
fulldata['AwayELO'] = elo_data['A_Team_Elo_After']

dummy = pd.get_dummies(fulldata, columns=['WLoc'])
fulldata['W_Home01'] = dummy['WLoc_A']

fulldata.to_csv('prediction_data.csv', index=False)


