import pandas as pd 
import os
import shutil
from scoreboard import ScoreboardSeries
from mappers import file_to_event_mapper, event_to_game_title_mapper

def series_id_to_stage_id(series_id):
    return series_id[:series_id.rfind('-')]

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

    # files_to_process = ['data-2019-08-18-champs.csv']

    out_dir = 'scoreboards'
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    dfs= []
    for fname in files_to_process:
        df = pd.read_csv('data/' + fname)
        df['end time'] = pd.to_datetime(df['end time'])
        df['game title'] = event_to_game_title_mapper[file_to_event_mapper[fname]]
        df['stage id'] = df['series id'].apply(series_id_to_stage_id, )
        print('data from event:', fname)
        num_series = len(df.groupby('series id'))
        print('num series:', num_series)
        num_games = len(df.groupby('match id'))
        print('num games:', num_games, '\n')


        event_dir = os.path.join(out_dir, file_to_event_mapper[fname].replace('/', '_').replace(' ', '_'))
        os.mkdir(event_dir)

        stage_groups = df.groupby('stage id')
        for stage_id, stage_group in stage_groups:

            out_file_name = os.path.join(event_dir, stage_id + '.txt')
            out_file = open(out_file_name, 'w')


            series_groups = stage_group.groupby('series id')
            series_groups = sorted(series_groups, key=lambda x: x[1].iloc[0]['end time'])
            for idx, (series_id, series_group) in enumerate(series_groups):
                sb = ScoreboardSeries(fname, series_group, idx)
                out_file.write(sb.to_string())
                out_file.flush()
            out_file.close()

        dfs.append(df)


    df = pd.concat(dfs)
    df.to_csv('all_data.csv', index=False)

if __name__ == '__main__':
    main()