import pandas as pd
import datetime
from pytz import timezone
from mappers import (
    mode_mapper,
    file_to_event_mapper,
    event_to_game_title_mapper,
    team_name_mapper,
    player_to_link_mapper,
    player_to_username_mapper
)

class ScoreboardSeries:
    def __init__(self, file_name, series_group):
        team1_raw, team2_raw = series_group['team'].drop_duplicates().to_list()
        self.team1 = team_name_mapper[team1_raw]
        self.team2 = team_name_mapper[team2_raw]
        self.game_title = event_to_game_title_mapper[file_to_event_mapper[file_name]]

        _, matches = zip(*series_group.groupby('match id'))
        matches = sorted(matches, key=lambda x: x.iloc[0]['end time'])

        first_match_finish = matches[0].iloc[0]['end time'].to_pydatetime()
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
            sbm = ScoreboardMatch(team1_raw, team2_raw, match, idx)
            self.scoreboard_matches.append(sbm)

    def to_string(self):
        result = '{{Box|start|padding=2em}}\n'
        result += f'{{{{Scoreboard/Header|{self.team1}|{self.team2}|title={self.game_title}'
        result += f'|date={self.date}|time={self.time}|timezone={self.timezone}|dst={self.dst}}}}}\n'
        for sbm in self.scoreboard_matches:
            result += sbm.to_string()
        result += '{{Box|end}}\n'
        return result


class ScoreboardMatch:
    def __init__(self, team1_raw, team2_raw, match_group, game_number):
        self.game_name = f'Game {game_number}'
        self.team1 = team_name_mapper[team1_raw]
        self.team2 = team_name_mapper[team2_raw]
        self.mode = mode_mapper[str(match_group.iloc[0]['mode'])]
        self.map = str(match_group.iloc[0]['map'])
        duration_seconds = int(match_group.iloc[0]['duration (s)'])
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        self.game_time = f'{minutes}:{seconds}'

        team1_players = match_group[match_group['team'] == team1_raw]
        team2_players = match_group[match_group['team'] == team2_raw]

        self.team1_score = int(team1_players.iloc[0]['score'])
        self.team2_score = int(team2_players.iloc[0]['score'])

        self.team1_sbs = []
        self.team2_sbs = []

        for _, team1_player in team1_players.iterrows():
            sbp = ScoreboardPlayer(team1_player, self.mode)
            self.team1_sbs.append(sbp)

        for _, team2_player in team2_players.iterrows():
            sbp = ScoreboardPlayer(team2_player, self.mode)
            self.team2_sbs.append(sbp)

    def to_string(self):
        result = f'{{{{Scoreboard|team1={self.team1}|team2={self.team2}|team1score={self.team1_score}|team2score={self.team2_score}\n'
        result += f'|gamename={self.game_name}|map={self.map}|gamemode={self.mode}|maptime={self.game_time}\n'

        for idx, sbp in enumerate(self.team1_sbs,1):
            result += f'|blue{idx}={sbp.to_string()}'
        for idx, sbp in enumerate(self.team2_sbs,1):
            result += f'|red{idx}={sbp.to_string()}'
        result += '}}\n'
        return result
        

class ScoreboardPlayer:
    def __init__(self, player_row, mode):
        self.mode = mode
        username_raw = str(player_row['player'])
        self.kills = int(player_row['kills'])
        self.deaths = int(player_row['deaths'])
        self.link = player_to_link_mapper[username_raw]
        self.username = player_to_username_mapper[username_raw]

        if self.link == username_raw:
            self.link = self.username

        if mode == 'Hardpoint':
            self.stats = {
                'time' : int(player_row['hill time (s)'])
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
                'caps' : int(player_row['ctf captures']),
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

    def to_string(self):
        result = f'{{{{Scoreboard/Player|name={self.username}|link={self.link}|kills={self.kills}|deaths={self.deaths}'
        for key, value in self.stats.items():
            result += f'|{key}={value}'
        return result + '}}\n'


