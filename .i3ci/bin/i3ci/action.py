import i3


class Action(object):
    ''' Define an i3-msg action. '''

    def __init__(self):
        self._actions = []

    def add(self, action, args=None):
        if args:
            action = action.__call__(self, *args)
        else:
            action = action.__call__(self)
        self._actions.append(action)
        return self

    def get_command(self):
        return ','.join(self._actions)

    def process(self):
        i3.msg('command', ','.join(self._actions))

    def exec_(self, app):
        return 'exec {0}'.format(app)

    def set_mode(self, mode):
        ''' Set the specified mode '''
        return 'mode "{0}"'.format(mode)

    def set_default_mode(self):
        ''' Set the default mode '''
        return self.set_mode('default')

    def jump_to_window(self, window):
        ''' Jump to the specified window. '''
        return '[con_id={0}] focus'.format(window)

    def jump_to_workspace(self, workspace):
        ''' Jump to the given workspace.
        Current used workspaces are prefixed with a dot '.'
        Workspace '`' means "back_and_forth" command.
        Workspace '=' is the scratch pad
        '''
        if workspace == '`':
            return "workspace back_and_forth"
        elif workspace == '=':
            return "scratchpad show"
        else:
            return "workspace {0}".format(workspace)

    def jump_to_mark(self, mark):
        ''' Jump to the given mark. '''
        return "[con_mark=\"{0}\"] focus".format(mark)

    def send_window_to_output(self, output):
        ''' Send the current window to the specified output. '''
        return "move to output {0}".format(output)

    def send_workspace_to_output(self, output):
        ''' Send the current workspace to the specified output. '''
        return "move workspace to output {0}".format(output)

    def send_window_to_workspace(self, workspace):
        ''' Send the current window to the passed workspace. '''
        if workspace == '`':
            return "move workspace back_and_forth"
        elif workspace == '=':
            return "move scratchpad"
        else:
            return "move workspace {0}".format(workspace)

    def focus_output(self, output):
        ''' Focus the specified output. '''
        return "focus output {0}".format(output)

    def focus_window(self, id_):
        ''' Focus the specified output. '''
        return "[con_id={0}] focus".format(id_)

    def mark_window(self, mark, id_=None):
        ''' Set the passed mark to the window with the passed id_.  '''
        if id_:
            return '[con_id={0}] mark "{1}"'.format(id_, mark)
        else:
            return 'mark "{0}"'.format(mark)

    def unmark_window(self, mark):
        ''' Disable the passed mark.  '''
        return 'unmark {0}'.format(mark)

    def rename_workspace(self, from_, to):
        ''' Rename the workspace '''
        return '\'rename workspace "{0}" to "{1}"\''.format(from_, to)

    def cmd(self, cmd):
        # wonderful method :-)
        return cmd


def default_mode(action=None):
    ''' Add or perform an action to set the default mode. '''
    if action:
        action.add(Action.set_default_mode)
    else:
        action = Action()
        action.add(Action.set_default_mode)
        action.process()
