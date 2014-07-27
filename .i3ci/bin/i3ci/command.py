from abc import ABCMeta, abstractmethod
import sys
import inspect
import os

import i3ci


class Command(object):
    ''' Base class for all i3ci commands.
    Note: The doc string of the commands derivated from this class
    are used as a description in the CLI.
    '''

    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self):
        ''' Process the command. '''

    def init_parser(self, parser):
        ''' Declare command specific subparsers and arguments. '''

    def validate_args(self, args):
        ''' Validate the arguments and return True if the command
        can be executed. '''
        return True


class Category(Command):
    ''' A category contains commands.
    Note: The doc string of the commands derivated from this class
    are used as a description in the CLI.
    '''

    __metaclass__ = ABCMeta

    def __init__(self, ppkg, ppkg_path, mname):
        self._ppkg = ppkg
        self._mpath = os.path.join(ppkg_path, mname)
        self._mname = '.'.join((ppkg, mname))
        self._cmds = {}

    def get_subcommands(self):
        mod = sys.modules[self._mname]
        classes = inspect.getmembers(
            mod, lambda x: inspect.isclass(x) and x.__module__ == self._mname)
        return [cls for name, cls in classes]

    def init_parser(self, parser):
        subparsers = parser.add_subparsers(
            title="Available sub-categories and commands",
            metavar='')
        cats = i3ci.create_categories_parser(
            subparsers, self._mname, self._mpath)
        cmds = self._add_commands(
            subparsers, [c() for c in self.get_subcommands()])
        self._cmds = dict(cats.items() + cmds.items())

    def validate_args(self, args):
        self._sel = [x for x in self._cmds.keys() if x in sys.argv]
        if self._sel:
            return self._cmds[self._sel[0]].validate_args(args)
        else:
            return False

    def process(self):
        sel = [x for x in self._cmds.keys() if x in sys.argv]
        if not sel:
            print('Error: no action specified.')
        else:
            self._cmds[sel[0]].process()

    def _add_commands(self, subparsers, commands):
        ''' Add parsers (sub commands) to this command. '''
        cmds = {}
        for c in commands:
            n = c.__class__.__name__
            p = subparsers.add_parser(
                n,
                help='[command] {0}'.format(c.__doc__),
                description=c.__doc__)
            c.init_parser(p)
            cmds[n] = c
        return cmds
