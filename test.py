import pandas as pd 
import os

fnames = os.listdir('data')
fnames = [fn for fn in fnames if '.csv' in fn]
dfs= []
cols = ["match id","series id","end time","duration (s)","mode","map","team","player","win?","score","kills","deaths","+/-"]
for fname in fnames:
    df = pd.read_csv('data/' + fname)
    print('data from event:', fname)
    num_series = len(df.groupby('series id'))
    print('num series:', num_series)
    num_games = len(df.groupby('match id'))
    print('num games:', num_games, '\n')


    df = df[cols]
    dfs.append(df)


df = pd.concat(dfs)
print(len(df))
print(len(df.columns))
print(df.columns)
print(len(df.groupby('match id')))
print(len(df.groupby('series id')))

print(df.groupby('mode').size())