''' i3 layout commands. '''
from i3ci import *


class default(command.Command):
    ''' Apply the default layout (tiling layout) to the current
    container. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('layout default',)).process()


class stacking(command.Command):
    ''' Apply the stacking layout to the current container. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('layout stacking',)).process()


class tabbed(command.Command):
    ''' Apply the tabbed layout to the current container. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('layout tabbed',)).process()


class toggle_split(command.Command):
    ''' Change the split direction of the current container (horizontal
    split or vertical split) '''

    def process(self):
        action.Action().add(action.Action.cmd,
                            ('layout toggle split',)).process()


class splith(command.Command):
    ''' Set the split direction for the current container to horizontal
    split. It means that new windows will be created at the right of the
    current window. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('layout splith',)).process()


class splitv(command.Command):
    ''' Set the split direction for the current container to vertical
    split. It means that new windows will be created at the bottom of the
    current window. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('layout splitv',)).process()
