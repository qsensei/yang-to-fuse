import os

from .utils import BaseTest
from .utils import here


def index(name):
    return {
        'name': name,
    }


def source(index, jsonpath):
    return {
        'index': index,
        'fuse:type': 'object',
        'attribute': jsonpath,
    }


class TestExampleTranslation(BaseTest):
    search_paths = (
        os.path.join(here, 'yangpath'),
    )
    models = (
        os.path.join(here, 'yangpath', 'example-sports.yang'),
        os.path.join(here, 'yangpath', 'example-stadium.yang'),
    )

    def test_depth_1(self):
        expected = {
            'defaults': {
                'limit': 5,
                'fulltext_index': 'tx',
            },
            'indexes': [
                {'name': 'tx', 'type': 'text'},
                index('birthday'),
                index('city'),
                index('gdp'),
                index('name'),
                index('number'),
                index('occupancy'),
                index('parties'),
                index('population'),
                index('scores'),
                index('season'),
                index('state'),
            ],
            'sources': [
                source('birthday', '$..birthday'),
                source('city', '$..city'),
                source('gdp', '$..example-sports:gdp'),
                source('gdp', '$..sports:gdp'),
                source('name', '$..name'),
                source('number', '$..number'),
                source('occupancy', '$..example-sports:occupancy'),
                source('occupancy', '$..sports:occupancy'),
                source('parties', '$..parties[*]'),
                source('population', '$..population'),
                source('scores', '$..scores'),
                source('season', '$..season'),
                source('state', '$..state'),
            ]
        }
        response = self.run_fut(
            search_paths=self.search_paths,
            models=self.models,
            max_depth=1,
        )
        assert expected == response

    def test_depth_2(self):
        expected = {
            'defaults': {
                'limit': 5,
                'fulltext_index': 'tx',
            },
            'indexes': [
                {'name': 'tx', 'type': 'text'},
                index('location_city'),
                index('location_gdp'),
                index('location_population'),
                index('location_state'),
                index('person_birthday'),
                index('person_name'),
                index('player_name'),
                index('player_number'),
                index('player_scores'),
                index('player_season'),
                index('politics_parties'),
                index('stadium_occupancy'),
                index('team_name'),
            ],
            'sources': [
                source('location_city', '$..location.city'),
                source('location_gdp', '$..location.example-sports:gdp'),
                source('location_gdp', '$..location.sports:gdp'),
                source('location_population', '$..location.population'),
                source('location_state', '$..location.state'),
                source('person_birthday', '$..person[*].birthday'),
                source('person_name', '$..person[*].name'),
                source('player_name', '$..player[*].name'),
                source('player_number', '$..player[*].number'),
                source('player_scores', '$..player[*].scores'),
                source('player_season', '$..player[*].season'),
                source('politics_parties',
                       '$..example-sports:politics.parties[*]'),
                source('politics_parties',
                       '$..sports:politics.parties[*]'),
                source('stadium_occupancy',
                       '$..stadium.example-sports:occupancy'),
                source('stadium_occupancy',
                       '$..stadium.sports:occupancy'),
                source('team_name', '$..team[*].name'),
            ]
        }
        response = self.run_fut(
            search_paths=self.search_paths,
            models=self.models,
            max_depth=2,
        )
        assert expected == response

    def test_depth_3(self):
        sl = 'stadium_location_'
        sp = 'sports_person_'
        tp = 'team_player_'
        st = 'sports_team_'
        sa = 'stadium_'
        expected = {
            'defaults': {
                'limit': 5,
                'fulltext_index': 'tx',
            },
            'indexes': [
                {'name': 'tx', 'type': 'text'},
                index('location_politics_parties'),
                index('sports_person_birthday'),
                index('sports_person_name'),
                index('sports_team_name'),
                index('stadium_location_city'),
                index('stadium_location_gdp'),
                index('stadium_location_population'),
                index('stadium_location_state'),
                index('stadium_occupancy'),
                index('team_player_name'),
                index('team_player_number'),
                index('team_player_scores'),
                index('team_player_season'),
            ],
            'sources': [
                source(
                    'location_politics_parties',
                    '$..location.example-sports:politics.parties[*]'),
                source(
                    'location_politics_parties',
                    '$..location.sports:politics.parties[*]'),
                source(sp + 'birthday', '$..sports.person[*].birthday'),
                source(sp + 'name', '$..sports.person[*].name'),
                source(st + 'name', '$..sports.team[*].name'),
                source(sl + 'city', '$..stadium.location.city'),
                source(sl + 'gdp', '$..stadium.location.example-sports:gdp'),
                source(sl + 'gdp', '$..stadium.location.sports:gdp'),
                source(sl + 'population', '$..stadium.location.population'),
                source(sl + 'state', '$..stadium.location.state'),
                source(sa + 'occupancy',
                       '$..stadium.example-sports:occupancy'),
                source(sa + 'occupancy',
                       '$..stadium.sports:occupancy'),
                source(tp + 'name', '$..team[*].player[*].name'),
                source(tp + 'number', '$..team[*].player[*].number'),
                source(tp + 'scores', '$..team[*].player[*].scores'),
                source(tp + 'season', '$..team[*].player[*].season'),
            ]
        }
        response = self.run_fut(
            search_paths=self.search_paths,
            models=self.models,
            max_depth=3,
        )
        assert expected == response

    def test_depth_4(self):
        sl = 'stadium_location_'
        sp = 'sports_person_'
        tp = 'sports_team_player_'
        st = 'sports_team_'
        sa = 'stadium_'
        expected = {
            'defaults': {
                'limit': 5,
                'fulltext_index': 'tx',
            },
            'indexes': [
                {'name': 'tx', 'type': 'text'},
                index('sports_person_birthday'),
                index('sports_person_name'),
                index('sports_team_name'),
                index('sports_team_player_name'),
                index('sports_team_player_number'),
                index('sports_team_player_scores'),
                index('sports_team_player_season'),
                index('stadium_location_city'),
                index('stadium_location_gdp'),
                index('stadium_location_politics_parties'),
                index('stadium_location_population'),
                index('stadium_location_state'),
                index('stadium_occupancy'),
            ],
            'sources': [
                source(sp + 'birthday', '$..sports.person[*].birthday'),
                source(sp + 'name', '$..sports.person[*].name'),
                source(st + 'name', '$..sports.team[*].name'),
                source(tp + 'name', '$..sports.team[*].player[*].name'),
                source(tp + 'number', '$..sports.team[*].player[*].number'),
                source(tp + 'scores', '$..sports.team[*].player[*].scores'),
                source(tp + 'season', '$..sports.team[*].player[*].season'),
                source(sl + 'city', '$..stadium.location.city'),
                source(sl + 'gdp', '$..stadium.location.example-sports:gdp'),
                source(sl + 'gdp', '$..stadium.location.sports:gdp'),
                source(sl + 'politics_parties', '$..stadium.location' +
                       '.example-sports:politics.parties[*]'),
                source(sl + 'politics_parties', '$..stadium.location' +
                       '.sports:politics.parties[*]'),
                source(sl + 'population', '$..stadium.location.population'),
                source(sl + 'state', '$..stadium.location.state'),
                source(sa + 'occupancy',
                       '$..stadium.example-sports:occupancy'),
                source(sa + 'occupancy',
                       '$..stadium.sports:occupancy'),
            ]
        }
        for n in xrange(4, 10):
            response = self.run_fut(
                search_paths=self.search_paths,
                models=self.models,
                max_depth=n,
            )
            assert expected == response
        response = self.run_fut(
            search_paths=self.search_paths,
            models=self.models,
        )
        assert expected == response
