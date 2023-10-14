import os
import subprocess as sp
import shutil
import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import random
import json
import datetime
import threading
import time

undolog = {}

RELEASE_NUMVER = 'v1.3'

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

class watchedPlaylist(tk.Frame):
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

def addPlaylist():
    pl_selected = filedialog.askopenfilename()
    if pl_selected is not None and len(pl_selected)>0:
        pl_selected = os.path.normpath(pl_selected)
        if os.path.exists(pl_selected) and pl_selected not in config['sourceDirs']:
            wp = watchedPlaylist(pl_selected,pathsFrame)
            wp.pack(anchor="n", side="top", expand='true',fill='x')
            watchedPaths.append(wp)
            config['sourceDirs'].append(pl_selected)


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

lastsortcol = config.get('lastsortcol',columns[0])
lastreverse = config.get('lastsortReversed',False)
def sorttree(col=None,reverse=False):
    global lastsortcol
    global lastreverse


    reverseafter = True
    if col is None:
        col = lastsortcol
        reverse = lastreverse
        reverseafter = False

    config['lastsortcol']=col
    config['lastsortReversed']=reverse

    lastsortcol = col
    lastreverse  = reverse

    if col == 'random':
        l = [(tree.set(k, 'filename'), k) for k in tree.get_children('')]
        random.shuffle(l)
    else:
        l = [(tree.set(k, col), k) for k in tree.get_children('')]
        l.sort(key=normsort,reverse=reverse)
    
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    if col != 'random' and reverseafter:
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

tempPlayer = ttk.Frame(framemain,padding=0,borderwidth=0,relief='flat',cursor='crosshair')
tempPlayer.grid(row=0, column=0, sticky='nsew')

playerFrames.append(tempPlayer)

player = mpv.MPV(wid=playerFrames[0].winfo_id(),
                 osc=True,
                 volume=config.get('initialvolume',60),
                 ytdl=True,
                 osd_on_seek='msg-bar',
                 script_opts='osc-layout=box,osc-seekbarstyle=knob,ytdl_hook-ytdl_path=yt-dlp.exe',
                 input_default_bindings=True,
                 input_vo_keyboard=True,
                 input_terminal=True,
                 scripts='osd.lua',
                 keep_open=True,
                 loop_file='inf',
                 mute=True)

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
initialseekspinLabel = ttk.Label(optionsframe,text="Initial Seek Offset % (-1=random)")
initialseekspinLabel.grid(row=0, column=0, sticky='NESW')
initialseekspin = ttk.Spinbox(optionsframe,textvariable=initialseekpcvar,increment=1, from_=-1, to=100)
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
xplayerCountLabel = ttk.Label(optionsframe,text="Multi Window Columns")
xplayerCountLabel.grid(row=2, column=0, sticky='NESW')
xplayerCountspin = ttk.Spinbox(optionsframe,textvariable=xplayerCountvar,increment=1, from_=1, to=5)
xplayerCountspin.grid(row=2, column=1, sticky='NESW')

yplayerCountvar = tk.StringVar()
yplayerCountLabel = ttk.Label(optionsframe,text="Multi Window Rows")
yplayerCountLabel.grid(row=3, column=0, sticky='NESW')
yplayerCountspin = ttk.Spinbox(optionsframe,textvariable=yplayerCountvar,increment=1, from_=1, to=5)
yplayerCountspin.grid(row=3, column=1, sticky='NESW')

layouts = [
    "Grid",
    "Grid",
    "Circle Pack",
    "Big Middle Grid",
    "Vert Stripe Grid",
    "Horiz Stripe Grid",
]

layoutvar   = tk.StringVar()
layoutvar.set(layouts[0])
layoutLabel = ttk.Label(optionsframe,text="Layout")
layoutLabel.grid(row=4, column=0, sticky='NEW')
layoutOpt = ttk.OptionMenu(optionsframe,layoutvar,*layouts)
layoutOpt.grid(row=4, column=1, sticky='NEW')

panScanvar   = tk.BooleanVar()
panScanLabel = ttk.Label(optionsframe,text="Fit Inner (pan scan)")
panScanLabel.grid(row=5, column=0, sticky='NEW')
panScanCheck = ttk.Checkbutton(optionsframe,var=panScanvar)
panScanCheck.grid(row=5, column=1, sticky='NEW')

osdvar   = tk.BooleanVar()
osdvar.set(config.get('showOSD',True))
osdLabel = ttk.Label(optionsframe,text="On Screen Display")
osdLabel.grid(row=6, column=0, sticky='NEW')
osdCheck = ttk.Checkbutton(optionsframe,var=osdvar)
osdCheck.grid(row=6, column=1, sticky='NEW')

switchCountvar = tk.StringVar()
switchCountvar.set('0')
switchCountLabel = ttk.Label(optionsframe,text="Switch timer (seconds)")
switchCountLabel.grid(row=7, column=0, sticky='NESW')
switchCountspin = ttk.Spinbox(optionsframe,textvariable=switchCountvar,increment=1, from_=1, to=float('inf'))
switchCountspin.grid(row=7, column=1, sticky='NESW')

loopsingleVar = tk.BooleanVar()
loopsingleVar.set(config.get('loopSingle',True))
loopsingleLabel = ttk.Label(optionsframe,text="Loop File")
loopsingleLabel.grid(row=8, column=0, sticky='NEW')
loopsingleCheck = ttk.Checkbutton(optionsframe,var=loopsingleVar)
loopsingleCheck.grid(row=8, column=1, sticky='NEW')

speedvar = tk.StringVar()
speedvar.set('1')
speedLabel = ttk.Label(optionsframe,text="Playback speed")
speedLabel.grid(row=9, column=0, sticky='NESW')
speedspin = ttk.Spinbox(optionsframe,textvariable=speedvar,increment=0.05, from_=0, to=50)
speedspin.grid(row=9, column=1, sticky='NESW')


editorVar = tk.StringVar()
editorVar.set( '|'.join(config.get('editor',[])) )
edtiorLabel = ttk.Label(optionsframe,text="External Editor")
edtiorLabel.grid(row=10, column=0, sticky='NESW')
edtiorEntry = ttk.Entry(optionsframe,textvariable=editorVar)
edtiorEntry.grid(row=10, column=1, sticky='NESW')

editorcwdVar = tk.StringVar()
editorcwdVar.set( config.get('editor_cwd',''))
edtiorcwdLabel = ttk.Label(optionsframe,text="External Editor CWD")
edtiorcwdLabel.grid(row=11, column=0, sticky='NESW')
edtiorcwdEntry = ttk.Entry(optionsframe,textvariable=editorcwdVar)
edtiorcwdEntry.grid(row=11, column=1, sticky='NESW')


def editorChange(*args):
    config['editor'] = editorVar.get().split('|')
editorVar.trace('w',editorChange)

def edtitorcwdChange(*args):
    config['editor_cwd'] = editorcwdVar.get()
editorcwdVar.trace('w',edtitorcwdChange)



def speedchange(*args):
    try:
        newspeed = str(float(speedvar.get()))
        for p in players:
            p.speed = newspeed
    except:
        pass

speedvar.trace('w',speedchange)

def loopsinglechange(*args):
    for player in players:
        if loopsingleVar.get():
            player.loop_file ='inf'
        else:
            player.loop_file = 'no'

loopsingleVar.trace('w',loopsinglechange)


def osdvischange(*args):
    for iplayer in players:
        if osdvar.get():
            iplayer.command('script-message','osd_mode','auto')
        else:
            iplayer.command('script-message','osd_mode','never')
    config['showOSD'] = osdvar.get()

osdvar.trace('w',osdvischange)
osdvar.set(config.get('showOSD',True))

def initialseekchange(*args):
    for iplayer in players:
        try:
            if initialseekpcvar.get() == '-1':
                iplayer.start = str(random.randint(0,100))+'%'
            else:
                player.start = initialseekpcvar.get()+'%'
        except Exception as e:
            print(e)
    config['initialSeekOffset'] = initialseekpcvar.get()

initialseekpcvar.trace('w',initialseekchange)
initialseekpcvar.set(config.get('initialSeekOffset','0'))

def initialscanvarchange(*args):
    config['scanAtStartup'] = bool(initialscanvar.get())

initialscanvar.trace('w',initialscanvarchange)
initialscanvar.set(bool(config.get('scanAtStartup',True)))

layoutvar.set(str(config.get('layout',layouts[0])))
xplayerCountvar.set(int(config.get('xplayerwindows',1)))
yplayerCountvar.set(int(config.get('yplayerwindows',1)))

def randomseekonPlaybackEnd(sourceplayer,name,value):
    global player
    ()
    if value == True:
        player = sourceplayer
        videoRandom()
        player.pause=False

player.observe_property('eof-reached',lambda n,e,p=player:randomseekonPlaybackEnd(p,n,e) )


from itertools import product

def playerclick(e):
    global playerFrames, players, currentFile, player
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

afterid = None

def hideCursors():
    for ipf in playerFrames:
        try:
            ipf.configure(cursor='none')
        except Exception as e:
            print(e)

def rootmotion(e):
    global sidewindowexpanded
    global lowerwindowexpanded
    global player
    global afterid

    for ipf in playerFrames:
        try:
            ipf.configure(cursor='@custom.cur')
        except:
            ipf.configure(cursor='crosshair')

    if afterid is not None:
        root.after_cancel(afterid)

    afterid = root.after(800,hideCursors)

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
                try:
                    player.command('script-message','osd_defocus')
                except Exception as e:
                    pass
                player = iplayer
                if len(players)>1:
                    player.command('script-message','osd_focus')
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
        offset = 30

    for playerframe,iplayer in zip(playerFrames,players):
        if e.widget == playerframe:
            player = iplayer
            try:
                if ctrl:
                    if e.delta > 0:
                        playlist_prev()
                    else:
                        playlist_next()                
                else:
                    if e.delta > 0:
                        iplayer.command('seek',str(offset),'relative')
                    else:
                        iplayer.command('seek',str(-offset),'relative')
            except Exception as e:
                print(e)

playerFrames[0].bind('<MouseWheel>',scrollfunc)
framemain.bind('<MouseWheel>',scrollfunc)
isStarting = True


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
        if not isStarting:
            tree.selection_set(currentFile)
            isinitialFile = False


player.observe_property('duration', propertyChange)
player.observe_property('path', propertyChange)

dimsstartup = True

def playersortFunc(pair):
    gi = pair[0].grid_info()
    return gi['row'],gi['column']


def playerDimsChange(*args):
    global playerFrames, players, currentFile, player
    x,y = 1,1
    try:
        x,y = int(xplayerCountvar.get()),int(yplayerCountvar.get())
    except Exception as e:
        print(e)
        return

    if x < 1:
        x = 1

    if y < 1:
        y = 1

    config['xplayerwindows'] = x
    config['yplayerwindows'] = y


    layoutname = layoutvar.get().strip()

    if layoutname not in layouts:
        layoutvar.set(layouts[0])
        return

    config['layout'] = layoutname

    targetcount = x*y


    if layoutname == "Big Middle Grid" and x>2 and y>2:
        targetcount = (x*2) + ((y-2)*2) + 1
    elif layoutname == "Vert Stripe Grid" and x>2:
        targetcount = (y*2) + 1
    elif layoutname == "Horiz Stripe Grid" and y>2:
        targetcount = (x*2) + 1
    elif layoutname == 'Circle Pack':
        targetcount = x*y
    else:
        layoutname = 'Grid'

    playersToReap = []

    while len(playerFrames) > targetcount:
        tempPlayer = playerFrames.pop()
        tempPlayer.grid_forget()
        tempPlayer.destroy()

        tempplayer  = players.pop()
        playersToReap.append(tempplayer)

    def reapPlayers():
        for p in playersToReap:
            try:
                p.stop()
            except Exception as e:
                print(e)
            
            try:
                p.terminate()
            except Exception as e:
                print(e)
            
            try:
                del p
            except Exception as e:
                print(e)
        
        playersToReap.clear()

    root.after(1,reapPlayers)

    while len(playerFrames) < targetcount:
        tempPlayer = ttk.Frame(framemain,padding=0,borderwidth=0,relief='flat',cursor='crosshair')
        tempPlayer.grid(row=0, column=0, sticky='nsew')
        tempPlayer.bind('<Button-1>',playerclick)

        tempPlayer.bind('<Motion>',rootmotion)
        tempPlayer.bind('<Button-1>',rootmotion)
        tempPlayer.bind('<B1-Motion>',rootmotion)
        tempPlayer.bind('<MouseWheel>',scrollfunc)

        playerFrames.append(tempPlayer)

        initialseek = initialseekpcvar.get()
        if initialseek == '-1':
            initialseek = str(random.randint(0,100))


        tempplayer = mpv.MPV(wid=tempPlayer.winfo_id(),
                         osc=True,
                         volume=config.get('initialvolume',60),
                         ytdl=True,
                         osd_on_seek='msg-bar',
                         script_opts='osc-layout=box,osc-seekbarstyle=knob,ytdl_hook-ytdl_path=yt-dlp.exe',
                         input_default_bindings=True,
                         input_vo_keyboard=True,
                         input_terminal=True,
                         scripts='osd.lua',
                         mute=True,
                         speed=speedvar.get(),
                         panscan=1 if panScanvar.get() else 0,
                         start=initialseek+'%',
                         keep_open=True,
                         loop_file='inf' if loopsingleVar.get() else 'no')

        if osdvar.get():
            tempplayer.command('script-message','osd_mode','auto')
        else:
            tempplayer.command('script-message','osd_mode','never')

        tempplayer.observe_property('duration', propertyChange)
        tempplayer.observe_property('path', propertyChange)
        tempplayer.observe_property('eof-reached',lambda n,e,p=tempplayer:randomseekonPlaybackEnd(p,n,e) )

        players.append(tempplayer)

        if not dimsstartup:
            if currentFile is not None:
                print('playing',currentFile)
                tempplayer.play(currentFile)
            else:
                print('playing',config['lastPlayed'])
                tempplayer.play(config['lastPlayed'])

    coords = []

    if layoutname == 'Big Middle Grid':
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

    elif layoutname == "Vert Stripe Grid":
        for yi in range(0,y):
            for xi in range(0,x):
                framemain.columnconfigure(xi, weight=1)
                framemain.rowconfigure(yi, weight=1)
                framemain.columnconfigure(xi+1, weight=0)
                framemain.rowconfigure(yi+1, weight=0)

        for yi in range(0,y):
            coords.append((0,yi,1,1))
            coords.append((x-1,yi,1,1))
            pass
        coords.append((1,0,x-2,y))
    elif layoutname == "Horiz Stripe Grid":
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
        coords.append((0,1,x,y-2))


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

    tplayerFrames,tplayers = zip(*sorted(zip(playerFrames, players),key=playersortFunc))

    playerFrames = list(tplayerFrames)
    players = list(tplayers)
    if player not in players:
        player = players[0]


xplayerCountvar.set(min(int(config.get('xplayerwindows',1)),4))
yplayerCountvar.set(min(int(config.get('yplayerwindows',1)),4))

xplayerCountvar.trace('w',playerDimsChange)
yplayerCountvar.trace('w',playerDimsChange)
layoutvar.trace('w',playerDimsChange)

layoutvar.set(str(config.get('layout',layouts[0])))

dimsstartup = False

def panscanChange(*args):
    config['panscan'] = panScanvar.get()
    for iplayer in players:
        if panScanvar.get():
            iplayer.panscan = 1
        else:
            iplayer.panscan = 0

panScanvar.trace('w',panscanChange)
panScanvar.set(bool(config.get('panscan',False)))

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

def savesearch():
    config['lastSearch'] = searchvar.get()
    dosearch()

lastSearch = None

def dosearch(force=False):
    global lastSearch

    needle = searchvar.get()
    print('dosearch',needle)
    if not force and lastSearch == needle:
        return
    
    lastSearch = needle

    needlesets = []
    for orbranch in needle.split('||'):
        orbranch = orbranch.strip()
        needles = [x.strip().upper() for x in orbranch.split(' ') if x.strip() != '' and all(c not in x for c in comparatorsymbols)]
        if len(needles) > 0:
            needlesets.append(needles)
    if len(needlesets) == 0:
        needlesets = [[]]

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

    currentwillberemoved = not any(all(n in currentFile.upper() for n in ns) for ns in needlesets)

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

        if any(all(n in plf.upper() for n in ns) for ns in needlesets):
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
    root.update_idletasks()

def rescan_async():
    global pl
    for directory in config['sourceDirs']:
        if os.path.isfile(directory):
            for line in open(directory,'r').readlines():
                stats = os.stat(directory)
                foundVideos[line] = {'path':line,
                                  'size':0,
                                  'playcount':0,
                                  'score':0,
                                  'createddate':stats.st_ctime,
                                  'size':0,
                                  'sorcescandir':directory}
        else:
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
                                    players[0].command('script-message','osd_message',f'Added {p}')
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
        if not os.path.exists(k) and not k.startswith('http'):
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
    dosearch(force=True)

def rescan():
    root.after(1,rescan_async)    
    

if config.get('scanAtStartup',False):
    rescan()

pl = sorted(list(foundVideos.items()))

pathsRescan = ttk.Button(pathsFrame,text='Rescan watched paths',command=rescan)
pathsRescan.pack(anchor="s", side="bottom", expand='true',fill='x',pady=1)

pathsAdd = ttk.Button(pathsFrame,text='Add new web playlist',command=addPlaylist)
pathsAdd.pack(anchor="s", side="bottom", expand='true',fill='x',pady=1)

pathsAdd = ttk.Button(pathsFrame,text='Add new watched path',command=addPath)
pathsAdd.pack(anchor="s", side="bottom", expand='true',fill='x',pady=1)




def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        path,_,_,_,_ = item['values']
        if path != currentFile:
            initialseek = initialseekpcvar.get()
            if initialseek == '-1':
                initialseek = str(random.randint(0,100))
                player.start = initialseek+'%'
            undolog.setdefault(id(player),[]).append((currentFile,player.time_pos))
            print('playing',path)
            player.play(path)
            player.video_pan_x=0
            player.video_pan_y=0
            player.video_scale_x = 1 
            player.video_scale_y = 1
            player.video_rotate=0
        break

tree.bind('<<TreeviewSelect>>', item_selected)


def drag(event):    
    x=event.x_root
    y=event.y_root
    targetwidget = root.winfo_containing(x,y)

    if targetwidget != event.widget and targetwidget in playerFrames and event.widget in playerFrames:

        sourceinfo  = event.widget.grid_info()
        target_info = targetwidget.grid_info()
        targetwidget.grid(**sourceinfo)
        event.widget.grid(**target_info)



root.bind("<B1-Motion>", drag)

searchvar.trace('w', lambda nm, idx, mode: savesearch())



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

    count = 0 
    for fn,dat in pl:
        if int(dat['score']) < 0:
            print('remove',fn,dat)
            try:
                os.remove(fn)
                count+=1
                player.command('script-message','osd_message',f'{fn} deleted')

            except Exception as e:
                print(e)
        else:
            temppl.append((fn,dat))
    pl = temppl
    dosearch()
    player.command('script-message','osd_message',f'{count} Files deleted')


def videoRandom(restrictions=None):
    try:
        children = list(tree.get_children())

        if restrictions is not None:
            tempchildren = children[:]
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

switchplayerind = 0
switchclock = 0

def switchFunc():
    global switchplayerind,switchclock,player
    while 1:
        try:
            time.sleep(0.1)
            switchCount = abs(int(float(switchCountvar.get())*10))
            if switchCount > 0 and len(players)>0:
                if switchclock%switchCount == 0:
                    player.command('script-message','osd_defocus')
                    player = players[switchplayerind%len(players)]
                    videoRandom()
                    if len(players)>1:
                        player.command('script-message','osd_focus')
                    switchplayerind+=1
                switchclock+=1
                switchclock = switchclock%switchCount
        except Exception as e:
            print(e)

switchthread = threading.Thread(target=switchFunc,daemon=True)
switchthread.start()


def videoVote(skip=False,increment=1):
    try:
        fn,score,pc,cdate,size = tree.item(currentFile, 'values')
        tree.item(currentFile, values=(fn,str(int(score)+(increment)),pc,cdate,size))
    except Exception as e:
        pass

    pldat = foundVideos.get(currentFile,{})
    pldat['score'] = pldat.get('score',0)+(increment)
    score = pldat['score']
    count = len(tree.get_children(''))
    player.command('script-message','osd_message',f'Video score {score} ({count})')
    dosearch(force=True)

    if skip:
        playlist_next()

def middlerandom(e):
    print(e.widget)
    if e.widget in playerFrames:
        player = players[playerFrames.index(e.widget)] 
        videoRandom()

root.bind('<Button-2>',middlerandom)
root.bind('<Button-3>',lambda x:playlist_next())

popout = None

def commandBackToLastPlayed(keysym,shift,ctrl):
    try:
        fn,tp = undolog.get(id(player),[]).pop()
        player.start = tp
        print('playing',fn)
        player.play(fn)
        player.time_pos = tp
        player.video_pan_x=0
        player.video_pan_y=0
        player.video_scale_x = 1 
        player.video_scale_y = 1
        player.video_rotate=0
    except Exception as e:
        print(e)

def commandRotateClockwise(keysym,shift,ctrl):
    pass

def commandRotateAntiClockwise(keysym,shift,ctrl):
    pass

commandMap = {
    'back-to-last-played':commandBackToLastPlayed,
    'rotate-clockwise':commandRotateClockwise,
    'rotate-anti-clockwise':commandRotateAntiClockwise,
}

def getBinding(binding,default):
    return config.get('bindings',{}).get(binding,default)

bindingsMap = {
    'back-to-last-played':getBinding('back-to-last-played','b'),
    'rotate-clockwise':'left',
    'rotate-anti-clockwise':'right',
}

def keyfunc(e):
    global fsstate
    global player
    global currentFile
    global popout

    global players
    global playerFrames

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
        player.command('script-message','osd_defocus')
        player.command('seek',str(ind),'absolute-percent')
    elif e.keysym.lower() == 'b':
        commandBackToLastPlayed(e.keysym,shift,ctrl)
    elif e.keysym.lower() == 'minus':
        pf = playerFrames[players.index(player)]
        grid_info = pf.grid_info()
        row = grid_info['row']
        col = grid_info['column']
        roww = pf.master.rowconfigure(row)['weight']
        colw = pf.master.columnconfigure(col)['weight']
        pf.master.rowconfigure(row,weight=max(1,roww-1))
        pf.master.columnconfigure(col,weight=max(1,colw-1))
    elif e.keysym.lower() == 'equal':
        pf = playerFrames[players.index(player)]
        grid_info = pf.grid_info()
        row = grid_info['row']
        col = grid_info['column']
        roww = pf.master.rowconfigure(row)['weight']
        colw = pf.master.columnconfigure(col)['weight']
        pf.master.rowconfigure(row,weight=roww+1)
        pf.master.columnconfigure(col,weight=colw+1)
    elif e.keysym.lower() == 'plus':
        pf = playerFrames[players.index(player)]
        grid_info = pf.grid_info()
        row = grid_info['row']
        col = grid_info['column']
        pf.master.rowconfigure(row,weight=1)
        pf.master.columnconfigure(col,weight=1)
    elif e.keysym.lower() == 'slash':
        player.video_pan_x = 0.0
        player.video_pan_y = 0.0
        player.video_scale_x = 1 
        player.video_scale_y = 1
        player.video_rotate = 0
    elif e.keysym.lower() == 'left':
        if ctrl:
            player.video_rotate = abs((player.video_rotate+2)%360)
        else:
            player.video_pan_x += 0.01
    elif e.keysym.lower() == 'right':
        if ctrl:
            player.video_rotate = abs((player.video_rotate-2)%360)
        else:
            player.video_pan_x -= 0.01
    elif e.keysym.lower() == 'down':
        if ctrl:
            player.video_scale_x -= 0.05
            player.video_scale_y -= 0.05
        else:
            player.video_pan_y -= 0.01
    elif e.keysym.lower() == 'up':
        if ctrl:
            player.video_scale_x += 0.05
            player.video_scale_y += 0.05
        else:
            player.video_pan_y += 0.01
    elif e.keysym.lower() == 'a':
        player.command('script-message','osd_defocus')
        player.command('seek',str(-offset),'relative')
        if ctrl:
            for iplayer in players:
                if iplayer != player:
                    iplayer.command('seek',str(-offset),'relative')
    elif e.keysym.lower() == 'd':
        player.command('script-message','osd_defocus')
        player.command('seek',str(offset),'relative')
        if ctrl:
            for iplayer in players:
                if iplayer != player:
                    iplayer.command('seek',str(offset),'relative')
    elif e.keysym.lower() == 'q':
        root.destroy()
    elif e.keysym.lower() == 'g':
        panScanvar.set(not panScanvar.get())
    elif e.keysym.lower() == 'm':
        for iplayer in players:
            player.command('script-message','osd_defocus')
            iplayer.mute = not iplayer.mute
            vol = iplayer.volume
            if iplayer.mute:
                iplayer.command('script-message','osd_message',f'🔇 {vol}')
            else:
                iplayer.command('script-message','osd_message',f'🔊 {vol}')
    elif e.keysym.lower() == 'r':
        sorttree('random',False)
        if ctrl:
            tempplayer = player
            restrictions = []
            for iplayer in players:
                iplayer.command('script-message','osd_defocus')
                player = iplayer
                item_selected(videoRandom(restrictions=restrictions))
        else:
            player.command('script-message','osd_defocus')
            videoRandom()
    elif e.keysym.lower() == 'e' and ctrl:
        cmd = []

        editor = config.get('editor',[])
        editorCwd = config.get('editor_cwd','.')

        if type(editor) == list:
            cmd += editor
        else:
            cmd += [editor]
        cmd += [currentFile]

        print(cmd)
        print(editorCwd)

        sp.Popen(cmd,cwd=editorCwd, start_new_session=True)
        if shift:
            root.destroy()
    elif e.keysym.lower() == 'e':
        player.command('script-message','osd_defocus')
        playlist_next()
    elif e.keysym.lower() == 'w':
        player.command('script-message','osd_defocus')
        playlist_prev()
    elif e.keysym.lower() == 'y':
        increment=1
        if shift:
            increment=2
        videoVote(skip=ctrl,increment=increment)
    elif e.keysym.lower() == 'u':
        increment=-1
        if shift:
            increment=-2
        videoVote(skip=ctrl,increment=increment)
    elif e.keysym.lower() == 'f' and ctrl:
        focusedplayer = player
        playerind = players.index(focusedplayer)
        focusedplayer = players.pop(playerind)
        focusedframe = playerFrames.pop(playerind)

        players = [focusedplayer]+players
        playerFrames = [focusedframe]+playerFrames

        while int(xplayerCountvar.get()) > 1:
            xplayerCountvar.set(int(xplayerCountvar.get())-1)

        while int(yplayerCountvar.get()) > 1:
            yplayerCountvar.set(int(yplayerCountvar.get())-1)

    elif e.keysym.lower() == 'f':
        fsstate = not fsstate
        root.attributes('-fullscreen',fsstate)
    elif e.keysym == 'space':
        player.pause = not player.pause
        if ctrl:
            for iplayer in players:
                iplayer.pause = player.pause
    elif e.keysym == '9':
        newvol = max(0,min(100,player.volume-5))
        targetplayers = [player]
        if ctrl:
            config['initialvolume'] = newvol
            targetplayers = players

        for tplayer in targetplayers:
            tplayer.volume = newvol
            vol = tplayer.volume
            if tplayer.mute:
                tplayer.command('script-message','osd_message',f'🔇 {vol}')
            else:
                tplayer.command('script-message','osd_message',f'🔊 {vol}')
    elif e.keysym == '0':
        newvol = max(0,min(100,player.volume+5))
        
        targetplayers = [player]
        if ctrl:
            config['initialvolume'] = newvol
            targetplayers = players

        for tplayer in targetplayers:
            tplayer.volume = newvol
            vol = tplayer.volume
            if tplayer.mute:
                tplayer.command('script-message','osd_message',f'🔇 {vol}')
            else:
                tplayer.command('script-message','osd_message',f'🔊 {vol}')
        
    elif e.keysym == 'c' and ctrl:
        if popout is None:
            popout = PopoutController(master=root)
        else:
            popout.destroy()
            popout = None
    elif e.keysym in ('z','comma'):
        ind = 0
        try:
            ind = players.index(player)
        except Exception as e:
            print(e)
        try:
            player.command('script-message','osd_defocus')
        except Exception as e:
            pass
        player = players[(ind-1)%len(players)]
        if len(players)>1:
            player.command('script-message','osd_focus')
    elif e.keysym in ('c','period'):
        ind = 0
        try:
            ind = players.index(player)
        except Exception as e:
            print(e)
        try:
            player.command('script-message','osd_defocus')
        except Exception as e:
            pass
        player = players[(ind+1)%len(players)]
        player.command('script-message','osd_focus')




framemain.bind('<KeyPress>',keyfunc)

class PopoutController(tk.Toplevel):
    def __init__(self, master=None, *args):
        tk.Toplevel.__init__(self, master)
        self.master = master
        
        self.title('Popout Controller')
        self.minsize(600,10)


        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(1, weight=1)

        self.attributes('-topmost', True)
        self.update()

        self.search = ttk.Entry(self,textvar=searchvar)
        self.search.grid(row=0, column=0, sticky='new')

        self.commandButton = ttk.Button(self,text='Click to Send Commands')
        self.commandButton.grid(row=1, column=0, sticky='nsew')
        self.commandButton.bind('<KeyPress>',keyfunc)

        self.commandButton.bind('<MouseWheel>',self.mousewheel)

        self.pushMessageVar = tk.StringVar()

        self.pushMessage = ttk.Entry(self,textvar=self.pushMessageVar)
        self.pushMessage.grid(row=2, column=0, sticky='new')

        self.pushMessage.bind('<Return>',self.pushmessagetext)
        self.template_instructions = """
        a,d - Forward and back
        w,e - Skip to next video
        ",","." - Skip between cells
        r - Random video
        ctrl-r - All random videos
        space - Pause
        ctrl-space -  Pause all
        ctrl-c -  Toggle popout
        """.strip()
       
        self.instructions = ttk.Label(self,text="Hover for shortcuts")
        self.instructions.grid(row=3, column=0, sticky='nsew')
        self.overrideredirect(True)

        xpos  = self.master.winfo_screenwidth()
        self.geometry("+{}+0".format(int((xpos/2)-(600/2))))

        self.instructions.bind('<Enter>',self.enterInstructions)
        self.instructions.bind('<Leave>',self.exitInstructions)

    def pushmessagetext(self,e):
        print(e)
        text = self.pushMessageVar.get()
        player.play(text)
        self.pushMessageVar.set('')

    def enterInstructions(self,e):
        self.instructions.configure(text=self.template_instructions)

    def exitInstructions(self,e):
        self.instructions.configure(text="Hover for shortcuts")

    def mousewheel(self,e):
        ctrl  = (e.state & 0x4) != 0
        shift = (e.state & 0x1) != 0

        o = lambda: None


        if ctrl and e.delta > 0:
            o.keysym = 'd'
            o.state = 0
            keyfunc(o)
        elif ctrl and e.delta < 0:
            o.keysym = 'a'
            o.state = 0
            keyfunc(o)
        elif shift and e.delta > 0:
            o.keysym = 'r'
            o.state = 0
            keyfunc(o)
        elif shift and e.delta < 0:
            o.keysym = 'r'
            o.state = 0
            keyfunc(o)
        elif e.delta > 0:
            o.keysym = 'period'
            o.state = 0
            keyfunc(o)
        elif e.delta < 0:
            o.keysym = 'comma'
            o.state = 0
            keyfunc(o)



lastplayed = config.get('lastPlayed','NONE')

searchvar.set(config.get('lastSearch',''))

if len(players)>1 and len(config.get('filehist',[])) > 1:
    for p,f in zip(players,filehist[::-1]):
        print('init',f)
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

buttondownvote  = ttk.Button(frameupper,text='▼ Downvote',command=lambda:videoVote(increment=-1))
buttondownvote.grid(row=0, column=2, sticky='nesw')

buttonupvote  = ttk.Button(frameupper,text='▲ Upvote',command=lambda:videoVote(increment=1))
buttonupvote.grid(row=0, column=3, sticky='nesw')

buttonnext  = ttk.Button(frameupper,text='Next >',command=playlist_next)
buttonnext.grid(row=0, column=4, sticky='nesw')

buttonclose  = ttk.Button(frameupper,text='Exit',command=close)
buttonclose.grid(row=0, column=5, sticky='nesw')

buttonDeleteLowScore = ttk.Button(frameupper,text='Delete videos with score < 0',
                                  command=deleteallLowScore)
buttonDeleteLowScore.grid(row=1, column=0, columnspan=6, sticky='nesw')

isStarting = False

root.mainloop()

json.dump(config,open('config.json','w'))
json.dump(foundVideos,open('videoCache.json','w'))