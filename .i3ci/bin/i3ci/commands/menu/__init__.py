'''
 Commands requiring the i3ci menu. To get the list of possible
action type "i3ci_cmd menu -h"
 '''
from subprocess import Popen

from i3ci import *
from i3ci.commands import do


# Application
# ----------------------------------------------------------------------------

class start_application(command.Command):
    '''Start an application on the specified monitor. The application is
    chosen via the i3ci menu. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)
        params.add_new_workspace_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        self._new = args.new
        return True

    def process(self):
        input_ = utils.applications_feed()
        size = utils.get_max_row(len(input_))
        proc = utils.create_menu(lmax=size)
        reply = proc.communicate(input_)[0]
        if reply:
            reply = reply.decode('utf-8')
            do.start_application.launch(reply, self._mon, self._new)
        else:
            action.default_mode()


# Workspaces
# ----------------------------------------------------------------------------

class create_workspace(command.Command):
    ''' Create a workspace by choosing a name from the i3ci workspace
    names catalog. The name is chosen via the i3ci menu. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        input_ = '\n'.join(utils.get_workspace_name_catalog())
        size = utils.get_max_row(len(input_))
        proc = utils.create_menu(lmax=size,
                                 lv=False,
                                 r=True,
                                 sb='#268bd2')
        reply = proc.communicate(input_)[0]
        if reply:
            a = action.Action()
            if self._mon != 'all':
                a.add(action.Action.focus_output, (self._mon,))
            a.add(action.Action.jump_to_workspace, (reply,))
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


class jump_to_workspace(command.Command):
    ''' Jump to an existing workspace. The workspace is chosen via the 
    i3ci menu. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        input_ = '\n'.join(utils.get_current_workspaces(self._mon))
        size = utils.get_max_row(len(input_))
        proc = utils.create_menu(lmax=size,
                                 r=True,
                                 sb='#268bd2')
        reply = proc.communicate(input_)[0]
        if reply:
            a = action.Action()
            a.add(action.Action.jump_to_workspace, (reply,))
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


class send_workspace_to_monitor(command.Command):
    ''' Send the current workspace to the specified monitor. The monitor is
    chosen via the i3ci menu. '''

    def process(self):
        # be sure that the workspace exists
        cur_wks = utils.get_current_workspace()
        if not cur_wks:
            return
        input_ = '\n'.join(
            sorted(utils.get_other_outputs())).encode('utf-8')
        size = utils.get_max_row(len(input_))
        proc = utils.create_menu(lmax=size,
                                 r=False,
                                 sb='#268bd2')
        reply = proc.communicate(input_)[0]
        if reply:
            reply = reply.decode('utf-8')
            output = utils.get_outputs_dictionary()[reply]
        a = action.Action()
        a.add(action.Action.send_workspace_to_output, (output,))
        action.default_mode(a)
        a.process()


# Windows
# ----------------------------------------------------------------------------

class jump_to_window(command.Command):
    ''' Jump to an existing window. The window is chosen via the
    i3ci menu.'''

    def init_parser(self, parser):
        params.add_monitor_param(parser)
        parser.add_argument('-i', '--instance',
                            default=None,
                            help='X window instance name.')

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        self._inst = args.instance
        return True

    def process(self):
        windows = utils.get_windows(self._inst, self._mon)
        win_names = sorted(windows.keys())
        size = utils.get_max_row(len(win_names))
        proc = utils.create_menu(lmax=size,
                                 sb='#b58900')
        win_name = proc.communicate('\n'.join(win_names).encode('utf-8'))[0]
        if win_name:
            win_name = win_name.decode('utf-8')
            a = action.Action()
            a.add(action.Action.jump_to_window, (windows[win_name],))
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


class jump_to_window2(command.Command):
    ''' Jump to an existing window using auto marks. The window is chosen
    via the i3ci menu.'''

    def process(self):
        marks = i3.msg('get_marks')
        size = utils.get_max_row(len(marks))
        proc = utils.create_menu(lmax=size,
                                 sb='#b58900')
        mark = proc.communicate('\n'.join(marks).encode('utf-8'))[0]
        if mark:
            mark = mark.decode('utf-8')
            a = action.Action()
            a.add(action.Action.jump_to_mark, (mark,))
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


class send_window_to_workspace(command.Command):
    ''' Send the current window to an active or new workspace
    on the specified monitor. The workspace name is chosen via the
    i3ci menu. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)
        params.add_new_workspace_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        self._new = args.new
        return True

    def process(self):
        input_ = []
        if self._new:
            input_ = '\n'.join(utils.get_free_workspaces())
        else:
            input_ = '\n'.join(utils.get_current_workspaces(self._mon))
        size = utils.get_max_row(len(input_))
        proc = utils.create_menu(lmax=size,
                                 lv=not self._new,
                                 r=True,
                                 sb='#6c71c4')
        reply = proc.communicate(input_)[0]
        if reply:
            a = action.Action()
            a.add(action.Action.send_window_to_workspace, (reply,))
            a.add(action.Action.jump_to_workspace, (reply,))
            if self._mon != 'all' and self._mon != utils.get_current_output():
                a.add(action.Action.send_workspace_to_output, (self._mon,))
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


class send_window_to_window(command.Command):
    ''' Send the current window next to a targeted window. The target
    window is chosen via the i3ci menu. Note that it is not guaranteed
    that the window will be right beside the target window, it is only
    guaranteed that it will be on the same workspace as the target
    window. '''

    def init_parser(self, parser):
        params.add_monitor_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        windows = utils.get_windows_on_other_workspaces(self._mon)
        win_names = sorted(windows.keys())
        size = utils.get_max_row(len(win_names))
        proc = utils.create_menu(lmax=size,
                                 sb='#b58900')
        win_name = proc.communicate('\n'.join(win_names).encode('utf-8'))[0]
        if win_name:
            win_id = windows[win_name]
            wks = utils.get_workspace_of_window(win_id)
            a = action.Action()
            a.add(action.Action.send_window_to_workspace, (wks,))
            a.add(action.Action.jump_to_workspace, (wks,))
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


class send_window_to_monitor(command.Command):
    ''' Send the current window to the specified monitor. The monitor is
    chosen via the i3ci menu. '''

    def process(self):
        input_ = '\n'.join(
            sorted(utils.get_other_outputs())).encode('utf-8')
        size = utils.get_max_row(len(input_))
        proc = utils.create_menu(lmax=size,
                                 r=False,
                                 sb='#268bd2')
        reply = proc.communicate(input_)[0]
        if reply:
            reply = reply.decode('utf-8')
            output = utils.get_outputs_dictionary()[reply]
        a = action.Action()
        a.add(action.Action.send_window_to_output, (output,))
        a.add(action.Action.focus_output, (output,))
        action.default_mode(a)
        a.process()


class bring_window(command.Command):
    ''' Bring the chosen window on the current workspace. The window is
    chosen via the i3ci menu'''

    def init_parser(self, parser):
        params.add_monitor_param(parser)

    def validate_args(self, args):
        self._mon = params.get_monitor_value(args)
        return True

    def process(self):
        windows = utils.get_windows_on_other_workspaces(self._mon)
        win_names = sorted(windows.keys())
        size = utils.get_max_row(len(win_names))
        proc = utils.create_menu(lmax=size,
                                 sb='#b58900')
        win_name = proc.communicate('\n'.join(win_names).encode('utf-8'))[0]
        if win_name:
            win_id = windows[win_name]
            wks = utils.get_current_workspace()
            other_wks = utils.get_window_workspace(win_id)
            a = action.Action()
            # switch focus to the window to bring
            a.add(action.Action.jump_to_workspace, (other_wks,))
            a.focus_window(win_id)
            # send the window to the original workspace
            a.add(action.Action.send_window_to_workspace, (wks,))
            a.add(action.Action.jump_to_workspace, (wks,))
            # make sure the new window is focused at the end
            a.focus_window(win_id)
            # print action.get_command()
            action.default_mode(a)
            a.process()
        else:
            action.default_mode()


# Others
# ----------------------------------------------------------------------------

class system(command.Command):
    ''' Logout, suspend, reboot or shutdown. The action is chosen
    via the i3ci menu. '''

    def process(self):
        proc = utils.create_menu(lmax=4,
                                 nb='#002b36',
                                 nf='#eee8dc',
                                 sb='#cb4b16',
                                 sf='#eee8d5')
        input_ = '\n'.join(['logout', 'suspend', 'reboot', 'shutdown'])
        reply = proc.communicate(input_)[0]
        if reply:
            a = action.Action()
            a.add(action.Action.set_mode, ("confirm {0} ?".format(reply),))
            a.process()
            proc = utils.create_menu(lmax=4,
                                     nb='#002b36',
                                     nf='#eee8dc',
                                     sb='#cb4b16',
                                     sf='#eee8d5')
            input_ = '\n'.join(['OK', 'Cancel'])
            conf = proc.communicate(input_)[0]
            if conf == 'OK':
                a = action.Action()
                action.default_mode(a)
                a.process()
                Popen('{0} --{1}'.format('i3ci_exit', reply), shell=True)
                return
        action.default_mode()
