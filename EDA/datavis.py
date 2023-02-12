import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

# BASIC CORRELATION; NO HOME VS AWAY

regszndata = pd.read_csv('/Users/isalyubimova/ballinsights/regszn_stats_team.csv')
corrRegSzn = regszndata.corr().round(3)
sns.heatmap(corrRegSzn, annot=True)

tourneystatsdata = pd.read_csv('/Users/isalyubimova/ballinsights/tourney_stats_team.csv')
corrTourney = tourneystatsdata.corr().round(3)
sns.heatmap(corrTourney, annot=True)

# SPLIT DATA INTO: HOME, AWAY, NEUTRAL
reg_data = pd.read_csv('/Users/isalyubimova/ballinsights/regteamgamestats.csv')

regszn_home = reg_data[reg_data['WLoc'] == 'H']
regszn_away = reg_data[reg_data['WLoc'] == 'A']
regszn_neutral = reg_data[reg_data['WLoc'] == 'N']

# CORRELATION MAP: HOME, AWAY, NEUTRAL

corrRegHome = regszn_home.corr().round(3)
sns.heatmap(corrRegHome, annot=True)

corrRegAway = regszn_away.corr().round(3)
sns.heatmap(corrRegAway, annot=True)

corrRegNeutral = regszn_neutral.corr().round(3)
sns.heatmap(corrRegNeutral, annot=True)

# SLR AND MLR, HOME VS AWAY SEPARATELY
X_home_ast = regszn_home['WAst']
X_home_thrPt = regszn_home['W3Pt%']
X_home_WDR = regszn_home['WDR']
y_home = regszn_home['WScore']

X_away_ast = regszn_away['WAst']
X_away_thrPt = regszn_away['W3Pt%']
X_away_WDR = regszn_away['WDR']
y_away = regszn_away['WScore']

# plot different individual variables
X1_plot = reg_data['WAst']
X2_plot = reg_data['W3Pt%']
y_plot = reg_data['WScore']

X_home_ast = sm.add_constant(X_home_ast)
X_away1 = sm.add_constant(X_away_ast)
X_home_3pt = sm.add_constant(X_home_thrPt)
X_away_3pt = sm.add_constant(X_away_thrPt)

lr_home_1 = sm.OLS(y_home, X_home_ast).fit()
lr_away_1 = sm.OLS(y_away, X_away_ast).fit()
lr_home_2 = sm.OLS(y_home, X_home_thrPt).fit()
lr_away_2 = sm.OLS(y_away, X_away_thrPt).fit()


plt.scatter(X1_plot, y_plot)
plt.plot(X_home_ast, 56.154 + 1.446*X_home_ast, label='Home')
plt.plot(X_away1, 58.416 + 1.28*X_away1, label='Away')

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.xlabel('Number of Assists by Winning Team')
plt.ylabel('Number of Points Scored by Winning Team')

plt.scatter(X2_plot, y_plot)
plt.plot(X_home_3pt, 63.463 + 41.99*X_home_3pt, label='Home')
plt.plot(X_away_3pt, 61.02 + 41.91*X_away_3pt, label='Away')

handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())
plt.xlabel('Percent of 3 Point Shots Made by Winning Team')
plt.ylabel('Number of Points Scored by Winning Team')
plt.show()

# multiple linear regression
Xall_home = regszn_home[['WAst', 'W3Pt%', 'WDR']]
Xall_away = regszn_away[['WAst', 'W3Pt%', 'WDR']]

mlr1 = LinearRegression()
mlr2 = LinearRegression()

mlr_home = mlr1.fit(Xall_home, y_home)
mlr_away = mlr2.fit(Xall_away, y_away)

