'''
Perform a simple command. To get the list of possible action type
"i3ci_cmd do -h"
 '''
import os
from subprocess import Popen, PIPE

from Xlib import display

from i3ci import *


# Application
# ----------------------------------------------------------------------------

class start_application(command.Command):
    '''Start an application on the specified monitor. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)
        params.add_new_workspace_param(parser)
        parser.add_argument(
            '-a', '--application',
            type=str,
            required=True,
            help=('Specify the application to launch. '
                  'i3ci_menu will not be launched.'))

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        self._new = args.new
        self._app = args.application
        return True

    def process(self):
        start_application.launch(self._app, self._mon, self._new)

    @staticmethod
    def launch(app, mon, in_new_wks):
        if '-cd' in app:
            xcwd = Popen('xcwd', stdin=PIPE, stdout=PIPE).communicate()[0]
            # TODO: replace all possible special characters
            xcwd = xcwd.replace('\n', '')
            special_chars = [' ', '(', ')']
            for c in special_chars:
                xcwd = xcwd.replace(c, r'\{0}'.format(c))
            app = '"' + app + ' ' + xcwd + '"'
        if not in_new_wks and (
                mon == 'all' or
                mon == utils.get_current_output()):
            # open on the current workspace
            a = action.Action()
            a.add(action.Action.exec_, (app,))
            action.default_mode(a)
            i3.subscribe('window', 'new',
                         utils.set_window_mark_callback,
                         lambda: a.process())
        if not in_new_wks and (
                mon != 'all' and
                mon != utils.get_current_output()):
            # open on the visible workspace on another output
            otherw = utils.get_current_workspace(mon)
            a = action.Action()
            a.add(action.Action.jump_to_workspace, (otherw,))
            a.add(action.Action.exec_, (app,))
            action.default_mode(a)
            i3.subscribe('window', 'new',
                         utils.set_window_mark_callback,
                         lambda: a.process())
        elif in_new_wks and (
                mon == 'all' or
                mon == utils.get_current_output()):
            # new workspace on the current output
            neww = utils.get_free_workspaces()[0]
            a = action.Action()
            a.add(action.Action.jump_to_workspace, (neww,))
            a.add(action.Action.exec_, (app,))
            action.default_mode(a)
            i3.subscribe('window', 'new',
                         utils.set_window_mark_callback,
                         lambda: a.process())
        elif in_new_wks and (
                mon != 'all' and
                mon != utils.get_current_output()):
            # new workspace on another output
            neww = utils.get_free_workspaces()[0]
            a = action.Action()
            a.add(action.Action.focus_output, (mon,))
            a.add(action.Action.jump_to_workspace, (neww,))
            a.add(action.Action.exec_, (app,))
            action.default_mode(a)
            i3.subscribe('window', 'new',
                         utils.set_window_mark_callback,
                         lambda: a.process())


# Workspaces
# ----------------------------------------------------------------------------

class focus_active_workspace(command.Command):
    ''' Focus the active workspace on the specified monitor. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser, mandatory=True)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        wks = utils.get_current_workspace(self._mon)
        a = action.Action()
        a.add(action.Action.jump_to_workspace, (wks,))
        action.default_mode(a)
        a.process()


class send_workspace_to_monitor(command.Command):
    ''' Send the current workspace to the specified monitor. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser, mandatory=True)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        a = action.Action()
        a.add(action.Action.send_workspace_to_output, (self._mon,))
        action.default_mode(a)
        a.process()


# Windows
# ----------------------------------------------------------------------------

class focus_window(command.Command):
    ''' Focus the nth window of the current workspace.
     Only the first 10 windows can be focused [0, 9]. '''

    def init_parser(self, parser):
        parser.add_argument(
            'index',
            type=int,
            choices=range(0, 10),
            help=('Window index. The order depends on the layout tree so '
                  'there is no simple rule to know which index corresponds '
                  'to which window, but indexes are easy to guess for simple '
                  'layout trees. Beware, the first window (top left) is at '
                  'index 1 and the index 0 is the 10nth window.'))
        parser.add_argument(
            '-w', '--workspace',
            required=False,
            default=None,
            type=str,
            help=('A workspace name. If not specified then the current '
                  'workspace is selected.'))

    def validate_args(self, args):
        self._args = args
        return True

    def process(self):
        wins = utils.get_windows_from_workspace(self._args.workspace)
        a = action.Action()
        nth = self._args.index
        if nth == 0:
            nth = 10
        a.add(action.Action.focus_window, (wins[nth-1],))
        a.process()


class send_window_to_monitor(command.Command):
    ''' Send the current window to the specified monitor. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser, mandatory=True)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        output = utils.get_outputs_dictionary()[self._mon]
        a = action.Action()
        a.add(action.Action.send_window_to_output, (output,))
        a.add(action.Action.focus_output, (output,))
        action.default_mode(a)
        a.process()


class send_window_to_new_workspace(command.Command):
    ''' Send the current window to a new workspace on the specified
    monitor. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        w = utils.get_free_workspaces()[0]
        a = action.Action()
        a.add(action.Action.send_window_to_workspace, (w,))
        a.add(action.Action.jump_to_workspace, (w,))
        if self._mon != 'all' and self._mon != utils.get_current_output():
            a.add(action.Action.send_workspace_to_output, (self._mon,))
        action.default_mode(a)
        a.process()


class send_window_to_monitor(command.Command):
    ''' Send the current window to the specified monitor. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser, mandatory=True)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        a = action.Action()
        a.add(action.Action.send_window_to_output, (self._mon,))
        a.add(action.Action.focus_output, (self._mon,))
        action.default_mode(a)
        a.process()


class clone_window(command.Command):
    ''' Clone the window by launching the same program as the current
    window. If the application is urxvt then the current working directory
    will be "cloned" as well. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)
        params.add_new_workspace_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        self._new = args.new
        return True

    def process(self):
        win = utils.get_current_window()[0]
        dpy = display.Display()
        xwin = dpy.create_resource_object('window', win['window'])
        inst, _ = xwin.get_wm_class()
        if inst:
            if inst == 'urxvt':
                inst += ' -cd'
            start_application.launch(inst, self._mon, self._new)
