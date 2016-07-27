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
    def test_example_models(self):
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
