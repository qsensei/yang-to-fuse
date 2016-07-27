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
        'type': 'object',
        'attribute': jsonpath,
    }


class TestTranslation(BaseTest):
    def test_simple(self):
        search_paths = []
        models = [os.path.join(here, 'simple.yang')]
        expected = {
            'indexes': [
                index('my-array'),
                index('my-array2'),
                index('my-attr'),
                index('my-attr2'),
            ],
            'sources': [
                source('my-array', '$..my-array[*]'),
                source('my-array2', '$..my-array2[*]'),
                source('my-attr', '$..my-attr'),
                source('my-attr2', '$..my-attr2'),
            ]
        }
        response = self.run_fut(
            search_paths=search_paths, models=models)
        assert expected == response

    def test_example_sports(self):
        search_paths = []
        models = [os.path.join(here, 'example-sports.yang')]
        expected = {
            'indexes': [
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
