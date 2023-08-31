import os
import shutil
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import random
import json
import datetime
import threading

RELEASE_NUMVER = 'v0.1'

config = {'sourceDirs':[]}

try:
    config = json.load(open('config.json','r'))
except Exception as e:
    print('Existing config not found')

scriptPath = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] = scriptPath + os.pathsep + os.environ["PATH"]

isinitialFile=True
currentFile = None
filehist = config.get('filehist',[])

import mpv

root = tk.Tk()
root.title('DePlayer')
root.minsize(1024,768)
root.attributes('-fullscreen',True)

root.style = ttk.Style()
root.style.theme_use('clam')

root.style.configure (".",color='white',foreground='#69bfdb',background='#0f0f0f',bordercolor='#000000',highlightbackground='#0f0f0f',troughcolor='#0f0f0f',border=0)
root.style.map('.',background=[('active', '#69bfdb'),('disabled', '#060B0C')], foreground=[('active', '#282828'),('disabled', '#4c4c4c')] )
root.style.configure ("TMenu",color='white',foreground='white',background='#0f0f0f',bordercolor='#000000',highlightbackground='#0f0f0f',troughcolor='#0f0f0f')
root.style.configure ("TToolbutton",color='white',foreground='white',background='#1f1f1f',activeforeground='white',activebackground='#1f1f1f',bordercolor='#1f1f1f',lightcolor='white',darkcolor='#1f1f1f',highlightbackground='#1f1f1f',highlightcolor='#282828')
root.style.configure ("TToolbutton.button",color='white',foreground='white',background='#1f1f1f',activeforeground='white',activebackground='#1f1f1f',bordercolor='#1f1f1f',lightcolor='white',darkcolor='#1f1f1f',highlightbackground='#1f1f1f',highlightcolor='#282828')
root.style.map('TToolbutton',background=[('active', '#1f1f1f')], foreground=[('active', '#282828')] )
root.style.map('TRadiobutton',background=[('active', '#1f1f1f')], foreground=[('active', '#282828')] )
root.style.map('TToolbutton.button',background=[('active', '#69bfdb')], foreground=[('active', '#282828')] )
root.style.configure ("TProgressbar.trough",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f',highlightbackground='#0f0f0f')
root.style.configure ("TMenu",color='white',foreground='white',background='#0f0f0f')
root.style.configure ("TNotebook",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f',highlightbackground='#0f0f0f')
root.style.configure ("TNotebook.Tab",borderwidth=0,color='white',foreground='#69bfdb',background='#0f0f0f',bordercolor='#0f0f0f',highlightbackground='#0f0f0f',border='flat',lightcolor='#0f0f0f')
root.style.map("TNotebook.Tab",
                            background=[("selected", '#2f2f2f'),("disabled", '#0f0f0f')], 
                            foreground=[("selected", 'white'),("disabled", '#0f0f0f')],
                            bordercolor=[("selected", '#2f2f2f'),("disabled", '#2f2f2f')]
                 )
root.style.configure ("TNotebook.Tab.Label",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f',highlightbackground='#0f0f0f',lightcolor='#0f0f0f')
root.style.configure ("TNotebook.label",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f',highlightbackground='#0f0f0f',lightcolor='#0f0f0f')
root.style.configure ("TNotebook.Pane",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f',highlightbackground='#0f0f0f')
root.style.configure ("TLabel",color='white',foreground='white',background='#0f0f0f')

root.style.configure ("TFrame",color='white',foreground='white',background='#0f0f0f',bordercolor='#1f1f1f',highlightbackground='#0f0f0f')

root.style.configure ("borderhilight.TFrame",color='#69bfdb',borderwidth='5',foreground='#69bfdb',background='#69bfdb',bordercolor='#69bfdb',highlightbackground='#0f0f0f')

root.style.configure ("TLabelframe",color='white',foreground='white',background='#0f0f0f',bordercolor='#1f1f1f',highlightbackground='#0f0f0f',relief='flat')
root.style.configure ("TLabelframe.Label",color='white',foreground='white',background='#0f0f0f',bordercolor='#1f1f1f')
root.style.configure ("TLabelframe.Frame",color='white',foreground='white',background='#0f0f0f',bordercolor='#1f1f1f',highlightbackground='#0f0f0f')
root.style.configure ("TButton",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f',activebackground='#282828',activeforeground='#282828',highlightcolor='#282828',lightcolor='#282828',darkcolor='#282828',fieldbackground='#282828',highlightbackground='#69bfdb')
root.style.map('TButton',background=[('active', '#69bfdb')], foreground=[('active', '#282828')] )
root.style.configure ("TCheckbutton",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f')
root.style.configure ("TCheckbutton.Label",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f')
root.style.configure ("TEntry",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f')
root.style.configure ("TMenubutton",color='white',foreground='white',background='#0f0f0f',bordercolor='#0f0f0f')
root.style.configure ("TSpinbox",color='white',foreground='white',fieldbackground='#1f1f1f',background='#0f0f0f',bordercolor='darkgrey',buttonbackground='white')
root.style.configure ("TEntry",color='white',foreground='white',fieldbackground='#1f1f1f',background='#0f0f0f',bordercolor='darkgrey')
root.style.configure ("TCombobox",color='white',foreground='white',fieldbackground='#0f0f0f',background='#0f0f0f',bordercolor='#0f0f0f')

root.style.configure ("Treeview",color='white',foreground='white',fieldbackground='#0f0f0f',background='#0f0f0f',bordercolor='#0f0f0f')


searchvar        = tk.StringVar()



framemain  = ttk.Frame(root,padding=0,borderwidth=0,relief='flat')
frameside  = ttk.Frame(root,padding=0,borderwidth=0,relief='flat')

frameupper = ttk.Frame(root,padding=0,borderwidth=0,relief='flat')

frameside.place( anchor='nw',relheight=1.0,relx=-1.0,relwidth=0.0)
framemain.place( anchor='nw',relheight=1.0,relx=0.0,relwidth=1.0 )

frameupper.place( anchor='nw',relheight=1.0,relx=-1.0,relwidth=1.0)

frameside.columnconfigure(0, weight=1)
frameside.rowconfigure(0, weight=1)

notebook = ttk.Notebook(frameside)
notebook.grid(row=0, column=0, sticky='nsew')


listingframe = ttk.Frame(notebook,padding=(0,12))
optionsframe = ttk.Frame(notebook,padding=12)



watchedPaths = []

class watchedPath(tk.Frame):
    
    def __init__(self, path, master):

        ttk.Frame.__init__(self, master)

        self.master=master
        self.path = path

        self.configure(relief='raised', border=1, borderwidth=1)

        self.pathframe = ttk.Frame(self)

        self.label = ttk.Label(self.pathframe,text=path)
        self.rembutton = ttk.Button(self.pathframe,text='Remove Path', command=self.rem)

        self.label.pack(anchor="nw", side="left", expand=True, fill='x')
        self.rembutton.pack(anchor="nw", side="right", expand=False, fill='x')


        self.pathframe.pack(anchor="sw", side="top", expand=False, fill='x')

        self.optionframe = ttk.Frame(self)

        self.allowDelete = ttk.Checkbutton(self.optionframe,text='Allow Deletion')
        self.allowDelete.pack(anchor="sw", side="left", expand=False, fill='x')

        self.removeNonVideo = ttk.Checkbutton(self.optionframe,text='Remove Non-Video files')
        self.removeNonVideo.pack(anchor="sw", side="left", expand=False, fill='x')


        self.removeEmptyDirs = ttk.Checkbutton(self.optionframe,text='Remove Empty Folders')
        self.removeEmptyDirs.pack(anchor="sw", side="left", expand=False, fill='x')


        self.optionframe.pack(anchor="sw", side="bottom", expand=True, fill='x')


    def rem(self):
        config['sourceDirs'].remove(self.path)
        watchedPaths.remove(self)
        self.destroy()

pathsFrame = ttk.LabelFrame(optionsframe,text='Watched Paths:', padding=8, relief='raised')

def addPath():
    folder_selected = filedialog.askdirectory()
    if folder_selected is not None:
        folder_selected = os.path.normpath(folder_selected)
        if os.path.exists(folder_selected) and folder_selected not in config['sourceDirs']:
            wp = watchedPath(folder_selected,pathsFrame)
            wp.pack(anchor="n", side="top", expand='true',fill='x')
            watchedPaths.append(wp)
            config['sourceDirs'].append(folder_selected)


for path in config['sourceDirs']:
    wp = watchedPath(path,pathsFrame)
    wp.pack(anchor="n", side="top", expand='true',fill='x')
    watchedPaths.append(wp)

pathsFrame.grid(row=20, column=0, columnspan=2, sticky='NESW', pady=16)



notebook.add(listingframe, text='Library')
notebook.add(optionsframe, text='Options')

listingframe.columnconfigure(0, weight=1)
listingframe.rowconfigure(0, weight=0)
listingframe.rowconfigure(1, weight=1)
listingframe.rowconfigure(1, weight=1)

search = ttk.Entry(listingframe,textvar=searchvar)
search.grid(row=0, column=0, sticky='nsew')

columns = ('filename', 'score', 'playcount', 'createddate', 'size')
tree = ttk.Treeview(listingframe, columns=columns, show='headings', selectmode='browse')

def datetimeparse(dt):
    return datetime.datetime.strptime(dt,'%Y-%m-%d')

def sizeof_fmt(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def sizetoBytes(sz, suffix="B"):
    mult = 1024
    for unit in ("K", "M", "G", "T", "P", "E", "Z"):
        try:
            if unit+suffix in sz:
                return float(sz.replace(unit+suffix,''))*mult
        except Exception as e:
            pass
        mult *= 1024
    return float(sz)


def normsort(v):
    for func in (float,int,datetimeparse,sizetoBytes):
        try:
            return func(v[0])
        except Exception as e:
            pass
    return v

lastsortcol = columns[0]
lastreverse = False
def sorttree(col=None,reverse=False):
    global lastsortcol
    global lastreverse


    reverseafter = True
    if col is None:
        col = lastsortcol
        reverse = lastreverse
        reverseafter = False
    
    lastsortcol = col
    lastreverse  = reverse

    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    l.sort(key=normsort,reverse=reverse)
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    if reverseafter:
        tree.heading(col, command=lambda: sorttree(col, not reverse))

tree.heading('filename', text='Filename', command = lambda c='filename': sorttree(c,False) )
tree.heading('score', text='Score', command = lambda c='score': sorttree(c,False) )
tree.heading('playcount', text='Playcount', command = lambda c='playcount': sorttree(c,False) )
tree.heading('createddate', text='Created', command = lambda c='createddate': sorttree(c,False) )
tree.heading('size', text='Size', command = lambda c='size': sorttree(c,False) )


tree.grid(row=1, column=0, sticky='nsew')
tree.column("score", minwidth=60, width=60, stretch='NO')
tree.column("playcount", minwidth=60, width=60, stretch='NO')
tree.column("createddate", minwidth=90, width=90, stretch='NO')
tree.column("size", minwidth=90, width=90, stretch='NO')


detailFrame = ttk.LabelFrame(listingframe,tex="Video Details")
detailFrame.grid(row=2, column=0, sticky='nsew')

playerFrames = []

framemain.columnconfigure(0, weight=1)
framemain.rowconfigure(0, weight=1)

tempPlayer = ttk.Frame(framemain,padding=0,borderwidth=0,relief='flat')
tempPlayer.grid(row=0, column=0, sticky='nsew')

playerFrames.append(tempPlayer)

player = mpv.MPV(wid=playerFrames[0].winfo_id(),
                 osc=True,
                 volume=40,
                 osd_on_seek='msg-bar',
                 script_opts='osc-layout=box,osc-seekbarstyle=knob',
                 input_default_bindings=True,
                 input_vo_keyboard=True,
                 input_terminal=True,
                 scripts='osd.lua',
                 mute=True,
                 loop_file='inf')

players = [player]

optionsframe.columnconfigure(0, weight=1)
optionsframe.columnconfigure(1, weight=1)

class wrappedOptionValue(ttk.Frame):

    def __init__(self,master,label,configname,inputclass,inputclassArgs={},changeCallback=None):
        self.var = tk.StringVar()
        self.master = master
        self.label = label
        self.configname = configname

        self.labelWidget = ttk.Label(self,text=label)
        self.inputWidget = inputclass(self,**inputclassArgs)

    def valuechange(*args):
        pass


optionsframe.rowconfigure(0, weight=0)
optionsframe.rowconfigure(1, weight=0)


initialseekpcvar = tk.StringVar()
initialseekspinLabel = ttk.Label(optionsframe,text="Initial Seek Offset %")
initialseekspinLabel.grid(row=0, column=0, sticky='NESW')
initialseekspin = ttk.Spinbox(optionsframe,textvariable=initialseekpcvar,increment=1, from_=0, to=100)
initialseekspin.grid(row=0, column=1, sticky='NESW')

initialscanvar   = tk.BooleanVar()
initialScanLabel = ttk.Label(optionsframe,text="Scan at startup")
initialScanLabel.grid(row=1, column=0, sticky='NEW')
initialScanCheck = ttk.Checkbutton(optionsframe,var=initialscanvar)
initialScanCheck.grid(row=1, column=1, sticky='NEW')

rightFramepcvar = tk.StringVar()
rightFramepcLabel = ttk.Label(optionsframe,text="Right Frame Size %")
rightFramepcLabel.grid(row=2, column=0, sticky='NESW')
rightFramepcspin = ttk.Spinbox(optionsframe,textvariable=rightFramepcvar,increment=1, from_=0, to=100)
rightFramepcspin.grid(row=2, column=1, sticky='NESW')

leftFramepcvar = tk.StringVar()
leftFramepcLabel = ttk.Label(optionsframe,text="Left Frame Size %")
leftFramepcLabel.grid(row=3, column=0, sticky='NESW')
leftFramepcspin = ttk.Spinbox(optionsframe,textvariable=leftFramepcvar,increment=1, from_=0, to=100)
leftFramepcspin.grid(row=3, column=1, sticky='NESW')

xplayerCountvar = tk.StringVar()
xplayerCountLabel = ttk.Label(optionsframe,text="Multi Window X count")
xplayerCountLabel.grid(row=2, column=0, sticky='NESW')
xplayerCountspin = ttk.Spinbox(optionsframe,textvariable=xplayerCountvar,increment=1, from_=1, to=8)
xplayerCountspin.grid(row=2, column=1, sticky='NESW')

yplayerCountvar = tk.StringVar()
yplayerCountLabel = ttk.Label(optionsframe,text="Multi Window Y count")
yplayerCountLabel.grid(row=3, column=0, sticky='NESW')
yplayerCountspin = ttk.Spinbox(optionsframe,textvariable=yplayerCountvar,increment=1, from_=1, to=8)
yplayerCountspin.grid(row=3, column=1, sticky='NESW')

bigMiddlevar   = tk.BooleanVar()
bigMiddleLabel = ttk.Label(optionsframe,text="Big Middle")
bigMiddleLabel.grid(row=4, column=0, sticky='NEW')
bigMiddleCheck = ttk.Checkbutton(optionsframe,var=bigMiddlevar)
bigMiddleCheck.grid(row=4, column=1, sticky='NEW')

def initialseekchange(*args):
    player.start = initialseekpcvar.get()+'%'
    for iplayer in players:
        iplayer.start = initialseekpcvar.get()+'%'
    config['initialSeekOffset'] = initialseekpcvar.get()

initialseekpcvar.trace('w',initialseekchange)
initialseekpcvar.set(config.get('initialSeekOffset','0'))

def initialscanvarchange(*args):
    config['scanAtStartup'] = bool(initialscanvar.get())

initialscanvar.trace('w',initialscanvarchange)
initialscanvar.set(bool(config.get('scanAtStartup',True)))

bigMiddlevar.set(bool(config.get('bigMiddle',False)))
xplayerCountvar.set(int(config.get('xplayerwindows',1)))
yplayerCountvar.set(int(config.get('yplayerwindows',1)))


from itertools import product

def playerclick(e):
    global playerFrames, players, currentFile, player
    print(playerFrames.index(e.widget))
    player = players[playerFrames.index(e.widget)]


playerFrames[0].bind('<Button-1>',playerclick)



def rightFramepcvarchange(*args):
    try:
        config['rightWidth'] = max(0.1,float(rightFramepcvar.get())/100)
    except Exception as e:
        print(e)

rightFramepcvar.trace('w',rightFramepcvarchange)
rightFramepcvar.set(config.get('rightWidth',0.25)*100)

def leftFramepcvarchange(*args):
    try:
        config['leftWidth'] = max(0.1,float(leftFramepcvar.get())/100)
    except Exception as e:
        print(e)

leftFramepcvar.trace('w',leftFramepcvarchange)
leftFramepcvar.set(config.get('leftWidth',0.25)*100)



sidewindowexpanded  = False
lowerwindowexpanded = False


def rootmotion(e):
    global sidewindowexpanded
    global lowerwindowexpanded
    global player

    leftwidth = config.get('leftWidth',0.25) 
    rightwidth = config.get('rightWidth',0.25)
    
    absx = e.x_root-root.winfo_rootx()
    nabsx = framemain.winfo_width()-(e.x_root-root.winfo_rootx())

    absy = e.y_root-root.winfo_rooty()
    nabsy = framemain.winfo_height()-(e.y_root-root.winfo_rooty())

    if nabsy < 175 and e.type == tk.EventType.ButtonPress and any(e.widget == x for x in playerFrames):
        player.command('seek',str(((e.x-55)/(framemain.winfo_width()-110)*100)),'absolute-percent')

    if nabsy < 175 and e.type == tk.EventType.Motion and (e.state & (1 << 8)) and any(e.widget == x for x in playerFrames):
        player.command('seek',str(((e.x-55)/(framemain.winfo_width()-110)*100)),'absolute-percent')

    if nabsy > 175 and absx < 120 and not sidewindowexpanded and not lowerwindowexpanded:
        sidewindowexpanded = True
        frameside.place( anchor='nw',relheight=1.0,relx=0.0,relwidth=leftwidth )
        framemain.place( anchor='nw',relheight=1.0,relx=leftwidth,relwidth=1-leftwidth)

    elif nabsy > 175 and nabsx < 120 and not sidewindowexpanded and not lowerwindowexpanded:
        lowerwindowexpanded=True
        frameupper.place( anchor='ne',relheight=1.0,relx=1.00,relwidth=rightwidth)
        framemain.place( anchor='nw',relheight=1.0,relx=0.0,relwidth=1-rightwidth)
        frameupper.focus_set()


    elif (lowerwindowexpanded or sidewindowexpanded) and any(e.widget == x for x in playerFrames):
        sidewindowexpanded = False
        lowerwindowexpanded = False
        frameside.place( anchor='nw',relheight=1.0,relx=-1.0,relwidth=0.0 )
        framemain.place( anchor='nw',relheight=1.0,relx=0.0,relwidth=1.0 )
        frameupper.place( anchor='ne',relheight=0.0,relx=-1.0,relwidth=1.0)
        framemain.focus_set()

    for playerframe,iplayer in zip(playerFrames,players):
        if e.widget == playerframe:
            if e.type == tk.EventType.ButtonPress:
                playerframe.configure(style="borderhilight.TFrame")
                player = iplayer
                player.command('script-message','osd_message',f'Selected')
            iplayer.command('script-message','osd_rootmotion')


root.bind('<Motion>',rootmotion)
root.bind('<Button-1>',rootmotion)
root.bind('<B1-Motion>',rootmotion)

def scrollfunc(e):
    global player
    offset = 10
    ctrl  = (e.state & 0x4) != 0
    shift = (e.state & 0x1) != 0

    if shift:
        offset = 1
    elif ctrl:
        offset = 30

    for playerframe,iplayer in zip(playerFrames,players):
        if e.widget == playerframe:
            player = iplayer
            player.command('script-message','osd_message',f'Selected')
            if e.delta > 0:
                iplayer.command('seek',str(offset),'relative')
            else:
                iplayer.command('seek',str(-offset),'relative')

playerFrames[0].bind('<MouseWheel>',scrollfunc)
framemain.bind('<MouseWheel>',scrollfunc)


def propertyChange(name,value):
    global isinitialFile
    global currentFile
    global filehist

    if name == 'path' and value is not None:
        currentFile = value
        filehist = filehist[-100:]
        if value not in filehist:
            filehist.append(value)
        config['lastPlayed'] = value
        config['filehist'] = filehist[-100:]
        if not isinitialFile:
            pldat = foundVideos.get(value,{})
            pldat['playcount'] = pldat.get('playcount',0)+1
            try:
                fn,score,pc,cdate,size = tree.item(currentFile, 'values')
                tree.item(currentFile, values=(fn,score,str(int(pc)+1),cdate,size))
            except Exception as e:
                pass
        tree.selection_set(currentFile)
        isinitialFile = False


player.observe_property('duration', propertyChange)
player.observe_property('path', propertyChange)

def playerDimsChange(*args):
    global playerFrames, players, currentFile
    x,y = 1,1
    try:
        x,y = int(xplayerCountvar.get()),int(yplayerCountvar.get())
    except Exception as e:
        print(e)
    print(x,y)

    if x < 1:
        x=1

    if y < 1:
        y = 1

    config['xplayerwindows'] = x
    config['yplayerwindows'] = y
    config['bigMiddle'] = bool(bigMiddlevar.get())

    usebigMiddleMode = bigMiddlevar.get()
    usebigMiddleMode = usebigMiddleMode and x>3 and y>3

    targetcount = x*y
    if usebigMiddleMode:
        targetcount = (x*2) + ((y-2)*2) + 1

    while len(playerFrames) > targetcount:
        tempPlayer = playerFrames.pop()
        tempPlayer.grid_forget()
        tempPlayer.destroy()

        tempplayer  = players.pop()
        try:
            tempplayer.terminate()
        except Exception as e:
            print(e)

        try:
            del tempplayer
        except Exception as e:
            print(e)


    while len(playerFrames) < targetcount:
        tempPlayer = ttk.Frame(framemain,padding=0,borderwidth=0,relief='flat')
        tempPlayer.grid(row=0, column=0, sticky='nsew')
        tempPlayer.bind('<Button-1>',playerclick)

        tempPlayer.bind('<Motion>',rootmotion)
        tempPlayer.bind('<Button-1>',rootmotion)
        tempPlayer.bind('<B1-Motion>',rootmotion)
        tempPlayer.bind('<MouseWheel>',scrollfunc)

        playerFrames.append(tempPlayer)

        tempplayer = mpv.MPV(wid=tempPlayer.winfo_id(),
                         osc=True,
                         volume=40,
                         osd_on_seek='msg-bar',
                         script_opts='osc-layout=box,osc-seekbarstyle=knob',
                         input_default_bindings=True,
                         input_vo_keyboard=True,
                         input_terminal=True,
                         scripts='osd.lua',
                         mute=True,
                         start=initialseekpcvar.get()+'%',
                         loop_file='inf')

        tempplayer.observe_property('duration', propertyChange)
        tempplayer.observe_property('path', propertyChange)

        players.append(tempplayer)
        
        if currentFile is not None:
            tempplayer.play(currentFile)
        else:
            tempplayer.play(config['lastPlayed'])


    coords = []
    
    if usebigMiddleMode:
        for yi in range(0,y):
            for xi in range(0,x):
                framemain.columnconfigure(xi, weight=1)
                framemain.rowconfigure(yi, weight=1)
                framemain.columnconfigure(xi+1, weight=0)
                framemain.rowconfigure(yi+1, weight=0)

        for xi in range(0,x):
            coords.append((xi,0,1,1))
            coords.append((xi,y-1,1,1))
            pass

        for yi in range(1,y-1):
            coords.append((0,yi,1,1))
            coords.append((x-1,yi,1,1))
            pass

        coords.append((1,1,x-2,y-2))

        print(coords)
    else:
        for yi in range(0,y):
            for xi in range(0,x):
                coords.append((xi,yi,1,1))
                framemain.columnconfigure(xi, weight=0)
                framemain.rowconfigure(yi, weight=0)
                framemain.columnconfigure(xi+1, weight=0)
                framemain.rowconfigure(yi+1, weight=0)

    for i,(xi,yi,spanx,spany) in enumerate(coords):
        try:
            tempPlayer = playerFrames[i]
            framemain.columnconfigure(xi, weight=1)
            framemain.rowconfigure(yi, weight=1)
            tempPlayer.grid(row=yi, column=xi, rowspan=spany, columnspan=spanx, sticky='nsew')
        except Exception as e:
            print(e)


xplayerCountvar.trace('w',playerDimsChange)
yplayerCountvar.trace('w',playerDimsChange)
bigMiddlevar.trace('w',playerDimsChange)

xplayerCountvar.set(int(config.get('xplayerwindows',1)))
yplayerCountvar.set(int(config.get('yplayerwindows',1)))
bigMiddlevar.set(bool(config.get('bigMiddle',False)))

framemain.focus_set()

import mimetypes
import subprocess as sp
import random
import json


foundVideos = {}

try:
    foundVideos = json.load(open('videoCache.json'))
except Exception as e:
    print(e)

pl = []


comparatorFuncs = {
    '!=':lambda a,b:a!=b, 
    '<':lambda a,b:a<b,
    '>':lambda a,b:a>b,
    '<=':lambda a,b:a<=b,
    '>=':lambda a,b:a>=b,
    '=':lambda a,b:a==b,
    '==':lambda a,b:a==b,
}

comparatorsymbols = sorted(comparatorFuncs.keys(),key=lambda x:len(x),reverse=True)

currentFile=''

def dosearch():
    needle = search.get()
    
    needles = [x.strip().upper() for x in needle.split(' ') if x.strip() != '' and all(c not in x for c in comparatorsymbols)]
    filters = [x.strip().upper() for x in needle.split(' ') if x.strip() != '' and any(c in x for c in comparatorsymbols)]
    filterset = {}
    for f in filters:
        try:
            comaparator = None
            for c in comparatorsymbols:
                if c in f:
                    comaparator = c
                    break
            if comaparator is not None:
                a,b = f.split(comaparator)
                compfunc = comparatorFuncs[comaparator]
                filterset[a]=(compfunc,int(b))
        except Exception as e:
            print(e)

    currentwillberemoved = not all([n in currentFile.upper() for n in needles])

    pldat = None

    if currentFile != '':
        for plf,tpldat in pl:
            if plf == currentFile:
                pldat = tpldat
                break

    if pldat is not None and len(filterset) > 0:
        for a,(c,b) in filterset.items():
            try:
                if not c(int(pldat.get(a.lower())) , b):
                    currentwillberemoved = True
                    break
            except Exception as eint:
                pass            

    try:
        nextfile = tree.next(currentFile)
    except:
        nextfile = None

    tree.delete(*tree.get_children())

    fileAdded = None

    for plf,pldat in pl:

        if all([n in plf.upper() for n in needles]):
            filtersPass = True
            for a,(c,b) in filterset.items():
                try:
                    if not c(int(pldat.get(a.lower())) , b):
                        filtersPass = False
                        break
                except Exception as eint:
                    pass
            if filtersPass:
                if fileAdded  is None:
                    fileAdded = plf

                create_time = datetime.datetime.fromtimestamp(pldat['createddate']).strftime('%Y-%m-%d')
                size = sizeof_fmt(pldat['size'])
                tree.insert('', tk.END, iid=plf, values=(pldat['path'],pldat['score'],pldat['playcount'],create_time,size))

    if currentwillberemoved:
        if nextfile is None and fileAdded is not None:
            tree.selection_set(fileAdded)
        elif nextfile is not None:
            try:
                tree.selection_set(nextfile)
            except Exception as e:
                print(e)

    sorttree()

def rescan_async():
    global pl
    for directory in config['sourceDirs']:
        for r,dl,fl in os.walk(directory):
            for f in fl:
                try:
                    p = os.path.join(r,f)
                    root.update_idletasks()
                    tg = mimetypes.guess_type(p)
                    if tg is not None and tg[0] is not None:
                        if 'video' in tg[0]:
                            if p not in foundVideos:
                                stats = os.stat(p)
                                foundVideos[p] = {'path':p,
                                                  'size':stats.st_size,
                                                  'playcount':0,
                                                  'score':0,
                                                  'createddate':stats.st_ctime,
                                                  'size':stats.st_size,
                                                  'sorcescandir':directory}
                                player.command('script-message','osd_message',f'Added {p}')
                        elif 'image' in tg[0]:
                            pass
                            #os.remove(p)
                            #print('Removed',tg,p)
                        else:
                            pass
                            #print('Bad',tg,p)
                except Exception as e:
                    print(e)
            #if len(fl) == 0 and len(dl) == 0:
            #    print('remdir',r)
            #    os.rmdir(r)

    for k,v in list(foundVideos.items()):
        if not os.path.exists(k):
            try:
                del foundVideos[k]
            except Exception as e:
                print(e)
        if v.get('sorcescandir') not in config['sourceDirs']:
            try:
                del foundVideos[k]
            except Exception as e:
                print(e)

    pl = sorted(list(foundVideos.items()))
    dosearch()

def rescan():
    root.after(1,rescan_async)    
    

if config.get('scanAtStartup',False):
    rescan()

pl = sorted(list(foundVideos.items()))

pathsRescan = ttk.Button(pathsFrame,text='Rescan watched paths',command=rescan)
pathsRescan.pack(anchor="s", side="bottom", expand='true',fill='x',pady=8)

pathsAdd = ttk.Button(pathsFrame,text='Add new watched path',command=addPath)
pathsAdd.pack(anchor="s", side="bottom", expand='true',fill='x',pady=8)


def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        path,_,_,_,_ = item['values']
        if path != currentFile:
            player.play(path)
        break

tree.bind('<<TreeviewSelect>>', item_selected)



searchvar.trace('w', lambda nm, idx, mode: dosearch())

dosearch()


fsstate = True

def playlist_prev():
    prevel = tree.prev(currentFile)
    tree.selection_set(prevel)
    tree.see(prevel)

def playlist_next():
    nextel = tree.next(currentFile)
    tree.selection_set(nextel)
    tree.see(nextel)

def deleteallLowScore():
    global pl
    temppl = []

    for fn,dat in pl:
        if int(dat['score']) < 0:
            print('remove',fn,dat)
            os.remove(fn)
        else:
            temppl.append((fn,dat))
    pl = temppl
    dosearch()

def videoRandom(restrictions=None):
    try:
        children = tree.get_children()

        if restrictions is not None:
            tempchildren = list(children[:])
            for e in restrictions:
                if e in tempchildren:
                    tempchildren.remove(e)
            if len(tempchildren)>0:
                children = tempchildren

        iidx = random.choice(children)
        tree.selection_set(iidx)
        tree.see(iidx)
        if restrictions is not None:
            restrictions.append(iidx)
    except Exception as e:
        print(e)

def videoDownvote(skip=False):
    try:
        fn,score,pc,cdate,size = tree.item(currentFile, 'values')
        tree.item(currentFile, values=(fn,str(int(score)-1),pc,cdate,size))
    except Exception as e:
        pass
    
    pldat = foundVideos.get(currentFile,{})
    pldat['score'] = pldat.get('score',0)-1
    score = pldat['score']
    player.command('script-message','osd_message',f'Video score {score}')
    dosearch()

    if skip:
        playlist_next()

def videoUpvote(skip=False):
    try:
        fn,score,pc,cdate,size = tree.item(currentFile, 'values')
        tree.item(currentFile, values=(fn,str(int(score)+1),pc,cdate,size))
    except Exception as e:
        pass

    pldat = foundVideos.get(currentFile,{})
    pldat['score'] = pldat.get('score',0)+1
    score = pldat['score']
    player.command('script-message','osd_message',f'Video score {score}')
    dosearch()

    if skip:
        playlist_next()

root.bind('<Button-2>',lambda x:playlist_prev())
root.bind('<Button-3>',lambda x:playlist_next())

def keyfunc(e):
    global fsstate
    global player
    global currentFile

    offset = 10
    ctrl  = (e.state & 0x4) != 0
    shift = (e.state & 0x1) != 0

    if shift:
        offset = 1
    elif ctrl:
        offset = 30

    seekpoints = [str(x) for x in range(1,9)]

    if e.keysym in seekpoints:
        ind = (seekpoints.index(e.keysym)/(len(seekpoints)))*100
        player.command('seek',str(ind),'absolute-percent')
    elif e.keysym.lower() == 'a':
        player.command('seek',str(-offset),'relative')
    elif e.keysym.lower() == 'd':
        player.command('seek',str(offset),'relative')
    elif e.keysym.lower() == 'q':
        root.destroy()
    elif e.keysym.lower() == 'm':
        for iplayer in players:
            iplayer.mute = not iplayer.mute
            vol = iplayer.volume
            if iplayer.mute:
                iplayer.command('script-message','osd_message',f'🔇 {vol}')
            else:
                iplayer.command('script-message','osd_message',f'🔊 {vol}')
    elif e.keysym.lower() == 'r':
        if ctrl:
            tempplayer = player
            restrictions = []
            for iplayer in players:
                player = iplayer
                item_selected(videoRandom(restrictions=restrictions))
        else:
            videoRandom()
    elif e.keysym.lower() == 'e':
        playlist_next()
    elif e.keysym.lower() == 'w':
        playlist_prev()
    elif e.keysym.lower() == 'y':
        videoUpvote(skip=ctrl)
    elif e.keysym.lower() == 'u':
        videoDownvote(skip=ctrl)
    elif e.keysym.lower() == 'f':
        fsstate = not fsstate
        root.attributes('-fullscreen',fsstate)
    elif e.keysym == 'space':
        player.pause = not player.pause
    elif e.keysym == '9':
        player.volume -= 5
        vol = player.volume
        if player.mute:
            player.command('script-message','osd_message',f'🔇 {vol}')
        else:
            player.command('script-message','osd_message',f'🔊 {vol}')
    elif e.keysym == '0':
        player.volume += 5
        vol = player.volume
        if player.mute:
            player.command('script-message','osd_message',f'🔇 {vol}')
        else:
            player.command('script-message','osd_message',f'🔊 {vol}')
    elif e.keysym == 'comma':
        ind = 0
        try:
            ind = players.index(player)
        except Exception as e:
            print(e)

        player = players[(ind-1)%len(players)]
        player.command('script-message','osd_message',f'ACTIVE')
    elif e.keysym == 'period':
        ind = 0
        try:
            ind = players.index(player)
        except Exception as e:
            print(e)
        player = players[(ind+1)%len(players)]
        player.command('script-message','osd_message',f'ACTIVE')


framemain.bind('<KeyPress>',keyfunc)


lastplayed = config.get('lastPlayed','NONE')

print(len(players),config.get('filehist',[]))
if len(players)>1 and len(config.get('filehist',[])) > 1:
    for p,f in zip(players,filehist[::-1]):
        p.play(f)
elif lastplayed is not None and tree.exists(lastplayed):
    tree.selection_set(lastplayed)
    tree.see(lastplayed)    
else:
    videoRandom()

def close():
    root.destroy()

frameupper.columnconfigure(0, weight=0)
frameupper.columnconfigure(1, weight=1)
frameupper.columnconfigure(2, weight=0)
frameupper.columnconfigure(3, weight=0)
frameupper.columnconfigure(4, weight=1)
frameupper.columnconfigure(5, weight=0)


buttondel  = ttk.Button(frameupper,text='Random',command=videoRandom)
buttondel.grid(row=0, column=0, sticky='nesw')


buttonprev  = ttk.Button(frameupper,text='< Prev',command=playlist_prev)
buttonprev.grid(row=0, column=1, sticky='nesw')

buttondownvote  = ttk.Button(frameupper,text='▼ Downvote',command=videoDownvote)
buttondownvote.grid(row=0, column=2, sticky='nesw')

buttonupvote  = ttk.Button(frameupper,text='▲ Upvote',command=videoUpvote)
buttonupvote.grid(row=0, column=3, sticky='nesw')

buttonnext  = ttk.Button(frameupper,text='Next >',command=playlist_next)
buttonnext.grid(row=0, column=4, sticky='nesw')

buttonclose  = ttk.Button(frameupper,text='Exit',command=close)
buttonclose.grid(row=0, column=5, sticky='nesw')

buttonDeleteLowScore = ttk.Button(frameupper,text='Delete videos with score < 0',
                                  command=deleteallLowScore)
buttonDeleteLowScore.grid(row=1, column=0, columnspan=6, sticky='nesw')


root.mainloop()

json.dump(config,open('config.json','w'))
json.dump(foundVideos,open('videoCache.json','w'))