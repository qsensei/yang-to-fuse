from collections import OrderedDict
from collections import namedtuple
import json
import logging

from pyang import plugin

LOG = logging.getLogger('yang-to-fuse')

Index = namedtuple('Index', ['name'])
Source = namedtuple('Index', ['index', 'type', 'attribute'])


def pyang_plugin_init():
    plugin.register_plugin(YangToFuse())


class YangToFuse(plugin.PyangPlugin):
    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts['qsensei-fuse'] = self

    def emit(self, ctx, modules, fd):
        indexes = set()
        sources = set()

        for module in modules:
            leaves = list(iter_leaves(module))
            for index in iter_indexes(leaves):
                indexes.add(index)
            for source in iter_sources(leaves):
                sources.add(source)

        indexes = sorted(indexes)
        indexes = [{'name': x.name} for x in indexes]
        indexes = [{'name': 'tx', 'type': 'text'}] + indexes

        sources = sorted(sources)
        sources = [{
            'index': x.index,
            'fuse:type': x.type,
            'attribute': x.attribute,
        } for x in sources]

        indexschema = OrderedDict()
        indexschema['defaults'] = {'fulltext_index': 'tx', 'limit': 5}
        indexschema['indexes'] = indexes
        indexschema['sources'] = sources
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
    for leaf in leaves:
        yield Index(as_index(leaf.arg))


def iter_sources(leaves):
    for leaf in leaves:
        yield Source(
            index=as_index(leaf.arg), type='object', attribute=get_path(leaf))


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
