from collections import OrderedDict
from itertools import chain
import json
import logging

from pyang import plugin

LOG = logging.getLogger('yang-to-fuse')


def pyang_plugin_init():
    plugin.register_plugin(YangToFuse())


class YangToFuse(plugin.PyangPlugin):
    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts['qsensei-fuse'] = self

    def emit(self, ctx, modules, fd):
        leaves = list(chain(*(iter_leaves(x) for x in modules)))
        indexschema = OrderedDict()
        indexschema['defaults'] = {'fulltext_index': 'tx', 'limit': 5}
        indexschema['indexes'] = [
            {'name': 'tx', 'type': 'text'}] + list(iter_indexes(leaves))
        indexschema['sources'] = sorted(
            iter_sources(leaves), key=lambda x: (x['index'], x['attribute']))
        fd.write(json.dumps(indexschema, indent=2))

    def add_opts(self, optparser):
        optlist = []
        g = optparser.add_option_group("qsensei-fuse output specific options")
        g.add_options(optlist)


def as_index(x):
    return x.replace('-', '_')


def iter_leaves(s):
    children = s.substmts
    children = filter(
        lambda x: x.keyword in (
            'grouping', 'container', 'leaf', 'leaf-list', 'list'),
        children
    )
    for child in children:
        if child.keyword == 'leaf' or child.keyword == 'leaf-list':
            yield child
        else:
            for leaf in iter_leaves(child):
                yield leaf


def iter_indexes(leaves):
    indexes = {x.arg for x in leaves}
    for index_name in sorted(indexes):
        yield {
            'name': as_index(index_name)
        }


def iter_sources(leaves):
    sources = set()
    for leaf in leaves:
        sources.add((leaf.arg, get_path(leaf)))
    for index, attr in sorted(sources):
        yield {
            'index': as_index(index),
            'fuse:type': 'object',
            'attribute': attr,
        }


def iter_parents(s):
    if s.parent is None:
        return
    for x in iter_parents(s.parent):
        yield x
    yield s.parent.arg


def get_path(leaf):
    if leaf.keyword == 'leaf':
        suffix = ''
    elif leaf.keyword == 'leaf-list':
        suffix = '[*]'
    else:
        raise ValueError('Unknown statement keyword type: {}'.format(
            leaf.keyword))
    return '$..{leaf}{suffix}'.format(
        leaf=leaf.arg, suffix=suffix)
