import string
import re
import thread
from subprocess import Popen, PIPE

from Xlib import display

import i3


# Outputs
# ----------------------------------------------------------------------------

def get_outputs_dictionary():
    ''' Returns a dictionary where key is a natural output name
    like "monitor 1" and value is the low level name like
    "xinerama-0"'''
    res = {}
    outputs = i3.msg('get_outputs')
    for i, o in enumerate(outputs):
        res['monitor {0}'.format(i+1)] = o['name']
    return res


def get_current_output():
    ''' Returns the current output name (the output with focus) '''
    workspaces = i3.msg('get_workspaces')
    workspace = i3.filter(tree=workspaces, focused=True)
    if workspace:
        return workspace[0]['output']
    else:
        return None


def get_other_outputs():
    ''' Return all the output names except the current output one. '''
    outs = get_outputs_dictionary()
    coutput = get_current_output()
    return [k for k, v in outs.iteritems() if v != coutput]


# Workspaces
# ----------------------------------------------------------------------------

def get_workspace_name_catalog():
    ''' Returns a raw list of all possible workspace names formed
    with one char. '''
    return ([str(x) for x in range(0, 10)] +
            [x for x in string.lowercase] +
            ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-',
             '_', '=', '+', '[', '{', ']', '}', '|', '\\', ';', ':',
             "'", '"', '.', '<', '>', '/', '?', '~', '`'])


def get_workspaces(mon='all'):
    ''' Returns a structure containing all the opened workspaces. '''
    used = []
    ws_tree = i3.msg('get_workspaces')
    outs = get_outputs_dictionary()
    for o in outs.itervalues():
        if mon == 'all' or mon == o:
            for ws in get_workspace_name_catalog():
                if i3.filter(tree=ws_tree, output=o, name=ws):
                    used.append(ws)
    used.append('`')
    return sorted(used)


def get_current_workspace(mon='all'):
    ''' Returns the current workspace name. '''
    workspaces = i3.msg('get_workspaces')
    if mon == 'all' or mon == get_current_output():
        return i3.filter(tree=workspaces, focused=True)[0]['name']
    else:
        return i3.filter(tree=workspaces, output=mon, visible=True)[0]['name']


def get_current_workspaces(mon='all'):
    ''' Returns a list of the names of all currently used workspaces on the
    specified output. '''
    all_ws = get_workspace_name_catalog()
    used = []
    ws_tree = i3.msg('get_workspaces')
    outs = get_outputs_dictionary()
    for o in outs.itervalues():
        if mon == 'all' or mon == o:
            for ws in all_ws:
                if i3.filter(tree=ws_tree, output=o, name=ws):
                    used.append(ws)
    return sorted(used)


def get_free_workspaces():
    ''' Returns the free workspace names as a list '''
    res = []
    all_workspaces = get_workspace_name_catalog()
    used_workspaces = i3.msg('get_workspaces')
    for wks in all_workspaces:
        if not i3.filter(tree=used_workspaces, name=wks):
            res.append(wks)
    return res


def get_workspace_of_window(win_id):
    ''' Returns the workspace name of the specified window. '''
    cworkspaces = get_current_workspaces()
    for wks in cworkspaces:
        ws_tree = i3.filter(name=wks)
        if i3.filter(tree=ws_tree, id=win_id):
            return wks
    return None


# Windows
# ----------------------------------------------------------------------------

def get_windows_from_workspace(ws):
    ''' Returns all the window IDs for the specified workspace. '''
    res = []
    if ws is None:
        ws = get_current_workspace()
    workspace = i3.filter(name=ws)
    if workspace:
        workspace = workspace[0]
        windows = i3.filter(workspace, nodes=[])
        for window in windows:
            res.append(window['id'])
    return res


def get_current_window():
    ''' Returns the current window structure. '''
    windows = i3.filter(nodes=[])
    return i3.filter(tree=windows, focused=True)


def get_current_window_id():
    ''' Returns the current window ID. '''
    window = get_current_window()
    if window:
        return window[0]['id']
    return ''


def set_window_mark_callback(event, data, subscription):
    ''' Callback to automatically set a mark on a created window. '''
    obj = 'container'
    con_id = None
    name = None
    window = None
    if event.setdefault(obj, None):
        con_id = event[obj].setdefault('id', None)
        name = event[obj].setdefault('name', None)
        window = event[obj].setdefault('window', None)
    if window:
        dpy = display.Display()
        xwin = dpy.create_resource_object('window', window)
        name, _ = xwin.get_wm_class()
    cnames = i3.msg('get_marks')
    if name in cnames:
        i = 1
        bname = name
        name = '{0}-{1}'.format(bname, i)
        while name in cnames:
            i += 1
            name = '{0}-{1}'.format(bname, i)
    if con_id and name:
        i3.msg('command', '[con_id={0}] mark "{1}"'.format(con_id, name))
    thread.interrupt_main()


def get_windows(win_inst=None, mon='all'):
    ''' Returns a dictionary of key-value pairs of a window text and
    window id.
    Each window text is of format "[instance] window title (instance number)"
    '''
    dpy = display.Display()
    res = {}
    lmax = 0
    for ws in get_current_workspaces(mon):
        workspace = i3.filter(name=ws)
        if not workspace:
            continue
        workspace = workspace[0]
        wname = workspace['name']
        windows = i3.filter(workspace, nodes=[])
        instances = {}
        # adds windows and their ids to the clients dictionary
        for window in windows:
            if window['window'] is None:
                continue
            xwin = dpy.create_resource_object('window', window['window'])
            inst, _ = xwin.get_wm_class()
            if inst:
                eligible = win_inst is None or win_inst == inst
                if eligible and mon != 'all':
                    # list only the windows on the specified output
                    id_ = window['id']
                    tree = i3.filter(name=mon)
                    eligible = i3.filter(tree, id=id_)
                if eligible:
                    win = window['name']
                    if win_inst:
                        win = u'({0}) {1}'.format(wname, win)
                    else:
                        if len(inst) + 2 > lmax:
                            lmax = len(inst) + 2
                        win = u'({0}) [{1}] {2}'.format(wname, inst, win)
                    # appends an instance number if other instances are
                    # present
                    if win in instances:
                        instances[win] += 1
                        win = '%s (%d)' % (win, instances[win])
                    else:
                        instances[win] = 1
                    res[win] = window['id']
    if lmax:
        res = _format_dict(res, lmax)
    return res


def _format_dict(d, lmax):
    ''' Align the window names. '''
    res = {}
    r = re.compile(r'(.*?)(\[.*?\])(.*)$')
    for k, v in d.iteritems():
        m = re.match(r, k)
        padding = lmax - len(m.group(2))
        if padding > 0:
            k = r.sub(r'\1\2' + ' '*padding + r'\3', k)
        res[k] = v
    return res


def get_window_ids(workspace):
    ''' Returns the windows IDs of the window contained on the specified
    workspace. '''
    res = []
    wks = i3.filter(name=workspace)
    wins = i3.filter(tree=wks, nodes=[])
    for w in wins:
        res.append(w['id'])
    return res


def get_windows_on_other_workspaces(mon):
    ''' Returns a list of tuple (text, win_id) of all the windows except
    the windows of the current workspace. '''
    windows = get_windows(mon=mon)
    excluded_wins = get_window_ids(get_current_workspace())
    if excluded_wins:
        # remove the wins of the current output from the list
        windows = {n: id_ for n, id_ in windows.iteritems()
                   if id_ not in excluded_wins}
    return windows


def get_window_workspace(win_id):
    cworkspaces = get_current_workspaces()
    for wks in cworkspaces:
        ws_tree = i3.filter(name=wks)
        if i3.filter(tree=ws_tree, id=win_id):
            return wks
    return None

# Menu
# ----------------------------------------------------------------------------

I3CI_MENU_MAX_ROW = 32
I3CI_MENU_HEIGHT = 18
I3CI_MENU_FONT = 'Ubuntu Mono-9:normal'


def create_menu(p=None,
                a=100,
                f=I3CI_MENU_FONT,
                lmax=8,
                lv=True,
                m=-1,
                h=I3CI_MENU_HEIGHT,
                r=False,
                nb='#002b36',
                nf='#657b83',
                sb='#859900',
                sf='#eee8d5'):
    ''' Returns a i3ci_menu process with the specified title and number
    of rows. '''
    cmd = ['i3ci_menu', '-f', '-i', '-lmax', str(lmax), '-y', '19',
           '-fn', f, '-nb', nb, '-nf', nf, '-sb', sb, '-sf', sf]
    if p:
        cmd.extend(['-p', p])
    if h:
        cmd.extend(['-h', str(h)])
    if r:
        cmd.append('-r')
    if lv:
        cmd.append('-lv')
    if a != 0:
        cmd.extend(['-a', str(a)])
    if m is not None and m != 'all' and m != -1:
        cmd.extend(['-m', str(m)])
    return Popen(cmd, stdin=PIPE, stdout=PIPE)


def applications_feed():
    ''' Returns a list of all found executables under paths. '''
    p = Popen('dmenu_path', stdout=PIPE, stderr=PIPE, shell=True)
    return p.stdout.read().encode('utf-8')


def get_max_row(rcount):
    return max([0, min([I3CI_MENU_MAX_ROW, rcount])])
