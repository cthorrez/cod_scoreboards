import pandas as pd
import json

A = ['Red Reserve', 'Tainted Minds', 'FaZe Clan', 'eUnited', 'Ghost Gaming']
B = ['Rise Nation', 'Team Kaliber', 'Luminosity', 'Epsilon', 'Enigma6']
C = ['Unilad', 'Mindfreak', 'Evil Geniuses', 'Echo Fox', 'Elevate']
D = ['OpTic Gaming', 'Splyce', 'Team EnVyUs', 'Complexity', 'Conquest']

def main():
    df = pd.read_csv('data/data-2018-06-17-anaheim.csv')
    df['pool'] = ''
    df['time'] = pd.to_datetime(df['end time'])
    pools = df[df['series id'].str.contains('pool')]
    pools.loc[pools['team'].isin(A), 'pool'] = 'A'
    pools.loc[pools['team'].isin(B), 'pool'] = 'B'
    pools.loc[pools['team'].isin(C), 'pool'] = 'C'
    pools.loc[pools['team'].isin(D), 'pool'] = 'D'
    print(len(pools[pools['pool']=='A']))
    print(len(pools[pools['pool']=='B']))
    print(len(pools[pools['pool']=='C']))
    print(len(pools[pools['pool']=='D']))

    pools = pools.sort_values(['series id', 'match id', 'team'])



    # pools = pools.drop(columns=['pool', 'time'])

    df = pd.concat([pools, df.tail(len(df) - len(pools))]).reset_index()
    print(len(df))

    match_nums = {'A' : set(), 'B' : set(), 'C' : set(), 'D' : set()}
    for idx, row in df.iterrows():
        print(idx)
        if 'pool' not in row['series id']:
            break

        fake_series_id = row['series id']
        real_pool = row['pool']
        match_nums[real_pool].add(fake_series_id)
        real_match_num = len(match_nums[real_pool]) - 1

        real_series_id = f'pool-{real_pool}-{real_match_num}'

        df.loc[idx,'series id'] = real_series_id


    print(len(df))
    df.to_csv('data/data-2018-06-17-anaheim_fixed.csv')

if __name__ == '__main__':
    main()