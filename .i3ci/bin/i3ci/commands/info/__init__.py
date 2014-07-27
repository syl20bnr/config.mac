'''
Get information. To get the list of the available commands type
"i3ci_cmd info -h"
 '''
from i3ci import *


# Outputs
# ----------------------------------------------------------------------------

class current_output(command.Command):
    ''' Output the name of the current output. '''

    def process(self):
        print utils.get_current_output()


# Workspaces
# ----------------------------------------------------------------------------

class workspace_name_catalog(command.Command):
    ''' Return a list of all possible one char workspace names. '''

    def process(self):
        print utils.get_workspace_name_catalog()


class current_workspace(command.Command):
    ''' Output the name of the current workspace. '''

    def init_parser(self, parser):
        params.add_monitor_param(
            parser,
            add_description=('An empty string is returned if the specified '
                             'monitor does not contain the current '
                             'workspace'))

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        workspace = utils.get_current_workspace(self._mon)
        if workspace:
            print workspace[0]['name']
        else:
            print ''


class used_workspaces(command.Command):
    ''' Output the names of all the currently used  workspaces. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        print utils.get_current_workspaces(self._mon)


class free_workspaces(command.Command):
    ''' Output free workspace names from the catalog. '''

    def process(self):
        print utils.get_free_workspaces()
