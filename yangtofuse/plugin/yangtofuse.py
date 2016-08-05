from collections import OrderedDict
from collections import namedtuple
from itertools import islice
import json
import logging
import optparse

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
        max_depth = ctx.opts.max_depth

        indexes = set()
        sources = set()

        for module in modules:
            leaves = list(iter_leaves(module))
            for index in iter_indexes(leaves, max_depth=max_depth):
                indexes.add(index)
            for source in iter_sources(leaves, max_depth=max_depth):
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
        optlist = [
            optparse.make_option(
                '--max-depth',
                default=None,
                dest='max_depth',
                type=int,
                help='''Depth (e.g. 3) to use when creating indexes.
                Complete path is default.
                '''
            ),
        ]
        g = optparser.add_option_group("qsensei-fuse output specific options")
        g.add_options(optlist)


def iter_hierarchy(x):
    yield x
    while x.parent and x.parent.keyword != 'module':
        yield x.parent
        x = x.parent


def as_index(x, max_depth):
    """ Convert node into a Fuse index.
    """
    hierarchy = list(islice(iter_hierarchy(x), 0, max_depth))
    hierarchy.reverse()
    return '_'.join(x.arg for x in hierarchy).replace('-', '_')


def iter_leaves(s):
    # yield leaves of children
    for child in s.i_children:
        if child.keyword in ('leaf', 'leaf-list'):
            yield child
        else:
            for leaf in iter_leaves(child):
                yield leaf


def iter_indexes(leaves, max_depth):
    for leaf in leaves:
        yield Index(as_index(leaf, max_depth))


def iter_sources(leaves, max_depth):
    for leaf in leaves:
        yield Source(
            index=as_index(leaf, max_depth),
            type='object',
            attribute=get_path(leaf, max_depth),
        )


def get_path(leaf, max_depth):
    if leaf.keyword not in ('leaf', 'leaf-list'):
        raise ValueError('Unknown statement keyword type: {}'.format(
            leaf.keyword))

    hierarchy = list(islice(iter_hierarchy(leaf), 0, max_depth))
    hierarchy.reverse()

    def iter_elements():
        yield '$.'
        for node in hierarchy:
            arg = get_node_name(node)
            if node.keyword in ('list', 'leaf-list'):
                yield '.{}[*]'.format(arg)
            else:
                yield '.{}'.format(arg)

    return ''.join(iter_elements())


def get_node_name(node):
    """ Get the name of the node.

    augments
    ========

    If the target of an augment statement AND ext:augment-identifier is
    defined, prefix the statement with the augmentation identifier.

    """
    arg = node.arg
    try:
        augment = node.i_augment
    except AttributeError:
        pass
    else:
        aug_id = augment.search_one(('yang-ext', 'augment-identifier'))
        if aug_id:
            arg = '{}:{}'.format(aug_id.arg, arg)
    return arg
