import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score
import pickle

df= pd.read_csv('2013-2022_cleaned.csv')
print(df.columns)
df.shape

#PREPROCESSING

df.dropna(inplace=True)

df['helper']=df['match_id']*df['innings']
df['current_wickets'] = (df.wicket).groupby(df.helper).cumsum()

print(df.columns)
df.shape

x= df[['venue', 'innings', 'ball','batting_team', 'bowling_team', 'runs', 'current_runs', 'wicket','current_wickets']]
y = df['TotalRuns']
print(x.shape)
x=pd.get_dummies(x,dtype='int')

x= df[['venue', 'innings', 'ball','batting_team', 'bowling_team', 'runs', 'current_runs', 'current_wickets']]
y = df['TotalRuns']
print(x.shape)
x=pd.get_dummies(x,dtype='int')

#x.to_csv('x.csv', index=False)
# print(y)

#MODEL TRAINING

train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.30)

regressor = RandomForestRegressor(n_estimators=50,min_samples_split=10)
regressor.fit(train_x, train_y)

p=regressor.predict(x)
r=r2_score(y,p)
print(r*100)

test_score = str(regressor.score(test_x, test_y)*100)
print(test_score)

print(np.mean(cross_val_score(regressor, train_x, train_y, cv=10)))

#PICKLE

pickle.dump(regressor,open('model.pkl','wb'))

model=pickle.load(open('model.pkl','rb'))

