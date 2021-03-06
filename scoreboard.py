import numpy as np
import pandas as pd
import datetime
import re
from pytz import timezone
from mappers import (
    mode_mapper,
    file_to_event_mapper,
    event_to_game_title_mapper,
    game_title_to_scoreboard_suffix_mapper,
    game_title_to_team2_color_mapper,
    team_name_mapper,
    player_to_link_mapper,
    player_to_username_mapper
)

def nan_safe_int(value):
    "converts a value to int, if it can't be converted, return empty string"
    try:
        return int(value)
    except:
        return ''

def seconds_converter(seconds, game_title):
    if game_title in  {'Black Ops 4', 'World War II'}:
        return int(seconds)
    elif game_title == 'Infinite Warfare':
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f'{minutes}:{str(seconds).rjust(2,"0")}'
    else:
        print(f'game title {game_title} unknown!')
        exit(1)

class ScoreboardSeries:
    def __init__(self, file_name, series_group, idx):
        self.idx = idx
        if len(series_group['team'].drop_duplicates().to_list()) != 2:
            for x in series_group['team'].drop_duplicates().to_list():
                print(x)
        team1_raw, team2_raw = series_group['team'].drop_duplicates().to_list()
        self.team1 = team_name_mapper[team1_raw]
        self.team2 = team_name_mapper[team2_raw]
        self.game_title = event_to_game_title_mapper[file_to_event_mapper[file_name]]

        _, matches = zip(*series_group.groupby('match id'))
        matches = sorted(matches, key=lambda x: x.iloc[0]['end time'])

        first_match_finish = matches[0].iloc[0]['end time'].to_pydatetime()

        if np.isnan(matches[0].iloc[0]['duration (s)']):
            first_match_duration = 0
        else:
            first_match_duration = int(matches[0].iloc[0]['duration (s)'])
        first_match_start = first_match_finish - datetime.timedelta(seconds=first_match_duration)
        first_match_start = first_match_start.astimezone(timezone('US/Pacific'))
        first_match_finish = first_match_finish.astimezone(timezone('US/Pacific'))
        
        self.date = first_match_start.strftime('%Y-%m-%d')
        self.time = first_match_start.strftime('%H%M')
        self.timezone = 'PST'
        dst_flag = bool(first_match_start.dst().seconds / 3600)
        self.dst = 'Yes' if dst_flag else 'No'

        self.scoreboard_matches = []
        for idx, match in enumerate(matches,1):
            sbm = ScoreboardMatch(team1_raw, team2_raw, match, idx, self.game_title)
            self.scoreboard_matches.append(sbm)

    def to_string(self):
        word = 'start' if self.idx % 2 == 0 else 'break'
        result = f'{{{{Box|{word}|padding=2em}}}}\n'
        result += f'{{{{Scoreboard/Header|{self.team1}|{self.team2}|title={self.game_title}'
        result += f'|date={self.date}|time={self.time}|timezone={self.timezone}|dst={self.dst}}}}}\n'
        for sbm in self.scoreboard_matches:
            result += sbm.to_string()
        if self.idx % 2 == 1:
            result += '{{Box|end}}'
        result += '\n'
        suffix = game_title_to_scoreboard_suffix_mapper[self.game_title]
        result = re.sub('Scoreboard', 'Scoreboard' + suffix, result)
        return result


class ScoreboardMatch:
    def __init__(self, team1_raw, team2_raw, match_group, game_number, game_title):
        self.game_name = f'Game {game_number}'
        self.team1 = team_name_mapper[team1_raw]
        self.team2 = team_name_mapper[team2_raw]
        self.game_title = game_title
        self.team2_color = game_title_to_team2_color_mapper[game_title]
        self.mode = mode_mapper[str(match_group.iloc[0]['mode'])]
        self.map = str(match_group.iloc[0]['map'])

        if not np.isnan(match_group.iloc[0]['duration (s)']):
            duration_seconds = int(match_group.iloc[0]['duration (s)'])
        else:
            duration_seconds = 0.0
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        self.game_time = f'{minutes}:{str(seconds).rjust(2,"0")}' if seconds > 0 else ''

        team1_players = match_group[match_group['team'] == team1_raw]
        team2_players = match_group[match_group['team'] == team2_raw]

        self.team1_score = int(team1_players.iloc[0]['score'])
        self.team2_score = int(team2_players.iloc[0]['score'])

        self.team1_sbs = []
        self.team2_sbs = []

        for _, team1_player in team1_players.iterrows():
            sbp = ScoreboardPlayer(team1_player, self.mode, self.game_title)
            self.team1_sbs.append(sbp)

        for _, team2_player in team2_players.iterrows():
            sbp = ScoreboardPlayer(team2_player, self.mode, self.game_title)
            self.team2_sbs.append(sbp)

    def to_string(self):
        result = f'{{{{Scoreboard|team1={self.team1}|team2={self.team2}|team1score={self.team1_score}|team2score={self.team2_score}\n'
        result += f'|gamename={self.game_name}|map={self.map}|gamemode={self.mode}|maptime={self.game_time}\n'

        for idx, sbp in enumerate(self.team1_sbs,1):
            result += f'|blue{idx}={sbp.to_string()}'
        for idx, sbp in enumerate(self.team2_sbs,1):
            result += f'|{self.team2_color}{idx}={sbp.to_string()}'
        result += '}}\n'
        return result
        

class ScoreboardPlayer:
    def __init__(self, player_row, mode, game_title):
        self.mode = mode
        self.game_title = game_title
        username_raw = str(player_row['player'])
        self.kills = int(player_row['kills'])
        self.deaths = int(player_row['deaths'])
        self.link = player_to_link_mapper[username_raw]
        self.username = player_to_username_mapper[username_raw]

        if self.link == username_raw:
            self.link = self.username

        if mode == 'Hardpoint':
            self.stats = {
                'time' : seconds_converter(player_row['hill time (s)'], self.game_title),
                'defends' : nan_safe_int(player_row['hill defends']),
            }
        elif mode == 'Search and Destroy':
            self.stats = {
                'plants' : int(player_row['bomb plants']),
                'defuses' : int(player_row['bomb defuses'])
            }
        elif mode == 'Control':
            self.stats = {
                'caps' : int(player_row['ctrl captures'])
            }
        elif mode == 'Capture the Flag':
            self.stats = {
                'captures' : int(player_row['ctf captures']),
                'returns' : int(player_row['ctf returns'])
            }
        elif mode == 'Uplink':
            self.stats = {
                'carries' : int(player_row['uplink dunks']),
                'throws' : int(player_row['uplink throws']),
                'score' : int(player_row['uplink points'])
            }
        else:
            print(f'got unrecognized game mode: {mode}')
            exit(1)
        if self.game_title == 'Infinite Warfare':
            self.stats.update({'icon' : player_row['fave payload']})

    def to_string(self):
        result = f'{{{{Scoreboard/Player|name={self.username}|link={self.link}|kills={self.kills}|deaths={self.deaths}'
        for key, value in self.stats.items():
            result += f'|{key}={value}'
        return result + '}}\n'


