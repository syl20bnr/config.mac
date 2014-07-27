'''
Common functions to declare and retrieve command line arguments.
'''
import re


def add_monitor_param(parser, mandatory=False, add_description=''):
    parser.add_argument(
        '-m', '--monitor',
        type=int,
        default=-1,
        required=mandatory,
        help=('An integer representing a monitor index, '
              '0 is the main monitor. '
              'Negative values stand for all the monitors. ' +
              add_description))


def get_monitor_value(args):
    mon = 'all'
    if args.monitor >= 0:
        mon = 'xinerama-{0}'.format(args.monitor)
    return mon


def get_natural_monitor_value(output):
    mon = output
    index = get_output_index(output)
    if index:
        mon = 'monitor {0}'.format(index + 1)
    return mon


def get_output_index(output):
    m = re.match('^xinerama-([0-9]+)$', output)
    if m:
        return int(m.group(1))
    return None


def add_new_workspace_param(parser, mandatory=False):
    parser.add_argument(
        '-n', '--new',
        action='store_true',
        default=False,
        required=mandatory,
        help=('The command is performed in a new workspace.'))
