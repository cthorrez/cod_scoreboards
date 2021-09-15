import pandas as pd 
import os
from scoreboard import ScoreboardSeries

def main():
    files_to_process = [
        'data-2017-08-13-champs.csv',
        'data-2018-04-08-proleague1.csv',
        'data-2018-04-19-relegation.csv',
        'data-2018-04-22-seattle.csv',
        'data-2018-07-29-proleague2.csv',
        'data-2018-06-17-anaheim.csv',
        'data-2019-01-20-proleague-qual.csv',
        'data-2019-07-05-proleague.csv',
        'data-2019-03-17-fortworth.csv',
        'data-2019-05-05-london.csv',
        'data-2019-06-16-anaheim.csv',
        'data-2019-07-21-proleague-finals.csv',
        'data-2019-08-18-champs.csv'
    ]

    files_to_process = ['data-2019-08-18-champs.csv']


    dfs= []
    for fname in files_to_process:
        df = pd.read_csv('data/' + fname)
        df['end time'] = pd.to_datetime(df['end time'])
        print('data from event:', fname)
        num_series = len(df.groupby('series id'))
        print('num series:', num_series)
        num_games = len(df.groupby('match id'))
        print('num games:', num_games, '\n')

        series_groups = df.groupby('series id')
        series_groups = sorted(series_groups, key=lambda x: x[1].iloc[0]['end time'])
        for series_id, series_group in series_groups:
            sb = ScoreboardSeries(fname, series_group)
            print(sb.to_string())



        dfs.append(df)


    df = pd.concat(dfs)
    df.to_csv('all_data.csv', index=False)

if __name__ == '__main__':
    main()