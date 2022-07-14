class MapperWrapper:
    """
    Utility function to wrap a dictionary
    If the requested key is in the dict, return the value associated with that key
    Otherwise just return the requested key back
    This is for when some but not all names line up between the Activision data and the names on the wiki
    """
    def __init__(self, mapper):
        self.mapper = mapper
    def __getitem__(self, item):
        if item in self.mapper:
            return self.mapper[item]
        else:
            return item

mode_mapper = MapperWrapper({
    'Capture The Flag' : 'Capture the Flag',
    'Search & Destroy' : 'Search and Destroy',
})

file_to_event_mapper = {
    'data-2017-08-13-champs.csv' : 'Call of Duty World League Championship 2017',
    'data-2018-04-01-birmingham.csv' : 'CWL Birmingham Open 2018',
    'data-2018-04-01-birmingham_argi.csv' : 'CWL Birmingham Open 2018',
    'data-2018-04-08-proleague1.csv' : 'CWL Pro League 2018 Stage 1',
    'data-2018-04-19-relegation.csv' : 'CWL Pro League 2018 Relegation',
    'data-2018-04-22-seattle.csv' : 'CWL 2018 Season Seattle Open',
    'data-2018-07-29-proleague2.csv' : 'CWL Pro League 2018 Stage 2',
    'data-2018-06-17-anaheim.csv' : 'CWL 2018 Season Anaheim Open',
    'data-2018-06-17-anaheim_fixed.csv' : 'CWL 2018 Season Anaheim Open',
    'data-2019-01-20-proleague-qual.csv' : 'CWL Pro League 2019 Qualifier',
    'data-2019-07-05-proleague.csv' : 'CWL Pro League 2019',
    'data-2019-03-17-fortworth.csv' : 'CWL Fort Worth 2019',
    'data-2019-05-05-london.csv' : 'CWL London 2019',
    'data-2019-06-16-anaheim.csv' : 'CWL Anaheim 2019',
    'data-2019-07-21-proleague-finals.csv' : 'CWL Pro League 2019 Playoffs',
    'data-2019-08-18-champs.csv' : 'Call of Duty World League Championship 2019'
}

event_to_game_title_mapper = {
    'Call of Duty World League Championship 2017' : 'Infinite Warfare',
    'CWL Birmingham Open 2018' : 'World War II',
    'CWL Pro League 2018 Stage 1' : 'World War II',
    'CWL Pro League 2018 Relegation' : 'World War II',
    'CWL 2018 Season Seattle Open' : 'World War II',
    'CWL Pro League 2018 Stage 2' : 'World War II',
    'CWL 2018 Season Anaheim Open' : 'World War II',
    'CWL Pro League 2019 Qualifier' : 'Black Ops 4',
    'CWL Pro League 2019' : 'Black Ops 4',
    'CWL Fort Worth 2019' : 'Black Ops 4',
    'CWL London 2019' : 'Black Ops 4',
    'CWL Anaheim 2019' : 'Black Ops 4',
    'CWL Pro League 2019 Playoffs' : 'Black Ops 4',
    'Call of Duty World League Championship 2019' : 'Black Ops 4'
}

game_title_to_scoreboard_suffix_mapper = {
    'Infinite Warfare' : 'IW',
    'World War II' : 'WWII',
    'Black Ops 4' : ''
}

game_title_to_team2_color_mapper = {
    'Infinite Warfare' : 'purple',
    'World War II' : 'purple',
    'Black Ops 4' : 'red'
}
    
team_name_mapper = MapperWrapper({
    'Epsilon' : 'Epsilon Esports EU',
    '3sUp' : '3sUP',
    'Mindfreak Black' : 'Mindfreak.Black',
    'Team EnVyUs' : 'Team Envy',
    'Team Infused' : 'Team infused',
    'eRa' : 'eRa Eternity',
    'Enigma6' : 'Enigma6 Group',
    'Unilad' : 'UNILAD Esports',
    'EZG Blue' : 'EZG.Blue',
    'Cyclone' : 'Cyclone EU',
    'Heretics' : 'Team Heretics',
    'Luminosity' : 'Luminosity Gaming',
    'Complexity' : 'Complexity Gaming',
    'Conquest' : 'Conquest Esports',
    'Brash' : 'Brash eSports',
    'Overtime' : 'Team Overtime	',
    'Imperial' : 'The Imperial',
    'Midnight' : 'Midnight Esports',
    'Reciprocity' : 'Team Reciprocity',
    'G2 eSports' : 'G2 Esports',
    'Giants' : 'Vodafone Giants',
    'ExcelerateGG' : 'Excelerate Gaming',
    'Riders' : 'Movistar Riders	',
    'Denial' : 'Denial Esports EU',
    'Excelerate' : 'Excelerate Gaming',
    'Celtic FC' : 'Celtic FC Esports',
    'RBL eSports' : 'Rebel Esports',
    'LGND Status GG' : 'LGND Status',
    'Animosity' : 'Animosity eSports',
    'Singularity' : 'Team Singularity',
    'Fury Gaming' : 'FURY Gaming',
    'TrainHard' : 'TrainHard Esport',
    'Optic' : 'Optic Gaming',
    'EvilGeniuses' : 'Evil Geniuses',
    'EchoFox' : 'Echo Fox',
    'TeamKaliber' : 'Team Kaliber',
    'RedReserve' : 'Red Reserve'
})

player_to_link_mapper = MapperWrapper({
    'Lucky' : 'Lucky (Alejandro López)',
    'Methodz' : 'Methodz (Anthony Zinni)',
    'Nova' : 'Nova (Dakota Williams)',
    'Reign' : 'Reign6',
    'Sukry' : 'Sukry (Endika Andres)',
    'Super' : 'Super (Tanner Bowen)',
    'Vortex' : 'Vortex (Stephen Allan)',
    'Yako' : 'YaKo (Iván Rodríguez)',
    'Zero' : 'Zer0'
})

player_to_username_mapper = MapperWrapper({
    'Abezy' : 'ABeZy',
    'Aches' : 'ACHES',
    'Alex' : 'Alexx',
    'Aqua' : 'AquA',
    'BBCONor' : 'BBConor',
    'Buzzo' : 'BuZZO',
    'Cells' : 'Mock',
    'Chino' : 'Cheen',
    'Colechan' : 'ColeChan',
    'Conor' : 'BBConor',
    'Crimsix' : 'C6',
    'DREEALL' : 'DREAL',
    'Enduraaa' : 'EndurAAA',
    'Envidian' : 'EnvdiaN',
    'Evas1on' : 'Evasion',
    'Fastballa' : 'FA5TBALLA',
    'Felony' : 'FeLo',
    'Formal' : 'FormaL',
    'GloFrosty' : 'Hamza',
    'Gunshiii' : 'Gunsiii',
    'Jetli' : 'JetLi',
    'Juju' : 'JuJu',
    'Kismet' : 'KiSMET',
    'Landxn' : 'Landxnn',
    'MethodZsick' : 'MethodZ (Jorge Bancells)',
    'Mettalz' : 'MettalZ',
    'Nameless' : 'NAMELESS',
    'Naux' : 'Hollow',
    'Nels' : 'Nelson',
    'Novo' : 'Nevo',
    'Priestah' : 'Priestahh',
    'Profeezy' : 'ProFeeZy',
    'Puni' : 'PuNi',
    'Replays' : 'Crowder',
    'Riskin' : 'RiskiN',
    'Rizk' : 'RizK',
    'Setzy' : 'Setzyy',
    'Shane' : 'ShAnE',
    'Silly' : 'SiLLY',
    'Slasher' : 'SlasheR',
    'SpaceLy' : 'Spacely',
    'Study' : 'StuDyy',
    'SyVortex' : 'Vortex (Brandon Gomes)',
    'TISCH47' : 'Tisch',
    'TJHaly' : 'TJHaLy',
    'Teddyrecks' : 'TeddyRecKs',
    'Tojor' : 'TojoR',
    'Turnup2ez' : 'TurnUp2eZ',
    'Wallers' : 'Wailers',
    'Zerg' : 'Deleo',
    'Zooma' : 'ZooMaa',
    'Zoomaa' : 'ZooMaa',
    'dReal' : 'DREAL',
    'detain' : 'Detain',
    'mosh' : 'Mosh',
})