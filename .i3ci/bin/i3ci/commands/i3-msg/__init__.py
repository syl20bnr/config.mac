''' Various i3 commands. This category is not very usefull since
you can already execute all the commands by calling directly the
"i3-msg" executable. But this category allows to interactively
discover the major commands offered by i3. Just navigate through the section
and invoke it with -h argument to get a list of possible commands. '''
from i3ci import *


class reload(command.Command):
    ''' Reload the config file. The i3 server is not restarted. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('reload',)).process()


class restart(command.Command):
    ''' Restart the i3 server. '''

    def process(self):
        action.Action().add(action.Action.cmd, ('restart',)).process()
