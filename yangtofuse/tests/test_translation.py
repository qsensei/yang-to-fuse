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


class TestTranslation(BaseTest):
    def test_simple(self):
        search_paths = []
        models = [os.path.join(here, 'simple.yang')]
        expected = {
            'defaults': {
                'limit': 5,
                'fulltext_index': 'tx',
            },
            'indexes': [
                {'name': 'tx', 'type': 'text'},
                index('my_array'),
                index('my_array2'),
                index('my_attr'),
                index('my_attr2'),
            ],
            'sources': [
                source('my_array', '$..my-array[*]'),
                source('my_array2', '$..my-array2[*]'),
                source('my_attr', '$..my-attr'),
                source('my_attr2', '$..my-attr2'),
            ]
        }
        response = self.run_fut(
            search_paths=search_paths, models=models)
        assert expected == response

    def test_example_sports(self):
        search_paths = []
        models = [os.path.join(here, 'example-sports.yang')]
        expected = {
            'defaults': {
                'limit': 5,
                'fulltext_index': 'tx',
            },
            'indexes': [
                {'name': 'tx', 'type': 'text'},
                index('birthday'),
                index('name'),
                index('number'),
                index('scores'),
                index('season'),
            ],
            'sources': [
                source('birthday', '$..birthday'),
                source('name', '$..name'),
                source('number', '$..number'),
                source('scores', '$..scores'),
                source('season', '$..season'),
            ]
        }
        response = self.run_fut(
            search_paths=search_paths, models=models)
        assert expected == response
