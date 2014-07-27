import sys
import os
import argparse

import i3
import params
import command
import utils
import action
__all__ = ['i3', 'params', 'command', 'utils', 'action']

# Constants
# ----------------------------------------------------------------------------

MODULE_NAME = os.path.splitext(os.path.basename(__file__))[0]
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
I3CI_CMD_PROG_NAME = 'i3ci-cmd'
I3CI_CMD_HOME_DIR = '.i3ci'
I3CI_CMD_HOME = os.path.join(os.path.expanduser("~"), I3CI_CMD_HOME_DIR)


# Main
# ----------------------------------------------------------------------------

def main():
    try:
        init_include_dirs()
        parser = init_parser()
        cmds = init_subparsers(parser)
        args = parser.parse_args()
        cmd = get_selected_cmd(cmds)
        if not cmd.validate_args(args):
            exit(1)
        cmd.process()
    except Exception:
        print('An error happened!')
        if 'args' not in locals() or args.debug:
            print_traceback()
        exit(1)


# Implementation
# ----------------------------------------------------------------------------

def init_include_dirs():
    sys.path.append(os.path.join(SCRIPT_PATH, 'lib'))


def init_parser():
    parser = argparse.ArgumentParser(
        prog=I3CI_CMD_PROG_NAME,
        version='%(prog)s version ' + '0.1',
        description=('i3 config improved Command Line Interface.'),
        epilog=('Support: sylvain.benner@gmail.com'))
    parser.add_argument(
        '--debug',
        action='store_true',
        help=('display the call stack if an exception is '
              'raised.'))
    return parser


def init_subparsers(parser):
    subparsers = parser.add_subparsers(
        title='Command categories',
        metavar='')
    return create_categories_parser(
        subparsers, "i3ci.commands", os.path.join(SCRIPT_PATH, "commands"))


def create_categories_parser(pparser, ppkg, ppkg_path):
    ''' Create a parser for each directory in ppkg_path.
    "p" prefix means "parent". '''
    category_classes = {}
    categories = [f for f in os.listdir(ppkg_path)
                  if os.path.isdir(os.path.join(ppkg_path, f))]
    for c in categories:
        cmds = __import__(ppkg, globals=globals(), fromlist=[c])
        mod = cmds.__dict__[c]
        cat = command.Category(ppkg, ppkg_path, c)
        parser = pparser.add_parser(
            name=c,
            help='[category] {0}'.format(mod.__doc__),
            description=mod.__doc__)
        cat.init_parser(parser)
        category_classes[c] = cat
    return category_classes


def get_selected_cmd(modules):
    sel = [x for x in modules.keys() if x in sys.argv]
    if not sel:
        print('Error: no command specified.')
        return None
    else:
        return modules[sel[0]]


def print_error(msg):
    print('Error: {0}'.format(msg))


def print_traceback():
    import traceback
    print traceback.format_exc()
