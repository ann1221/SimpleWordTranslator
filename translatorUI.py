# -*- coding: utf-8 -*-
import googleTransCore
from tkinter import *
from PIL import Image as Image
import PIL.ImageTk as ImageTk
from tkinter import simpledialog
from tkinter import messagebox
import json
import os
import sys

CONFIG = {}

class Application(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.translator = googleTransCore.Google_Translator()
        self.isAppCanChangeLocation = False
        self.isExpandedMore = False
        self.isTrackHistory = BooleanVar()

        self.configureRoot()
        self.createBasicVidgs()
        self.placeBasicVidgs()
        self.bindBasicEvents()
        self.fillLangListBox()
        
    def configureRoot(self):
        config = CONFIG['root']
        self.root.geometry("{0}+{1}".format(config['size'], config['position'])) 
        self.root.title(config['title'])
        self.root.resizable(config['resizable']['x'],config['resizable']['y'])
        self.root.overrideredirect(config['overrideredirect'])
        self.root.iconbitmap(CONFIG['paths']['icon'])

    def createBasicVidgs(self):
        styles = CONFIG['styles']
        infoText = CONFIG['infoUI']
        
        self.pad = Canvas(root)
        self.bgImage = ImageTk.PhotoImage(Image.open(CONFIG['paths']['bgImg']))
        self.imagesprite = self.pad.create_image(0, 0, image=self.bgImage)
        self.middleFrame = Frame(self.pad, 
                            bg = styles['primaryBg'], 
                            highlightbackground = styles['primaryFg'],
                            highlightcolor = styles['primaryFg'],
                            highlightthickness = 1)
        self.entryInp = Entry( self.middleFrame, 
                            validate="focusin", 
                            bg = styles['additionalBg'],
                            fg = styles['primaryFg'],
                            font = styles["font"])
        self.entryOutp = Entry(self.middleFrame, 
                            bg = styles['additionalBg'],
                            fg = styles['primaryFg'],
                            font = styles["font"])
        self.btnTranslate = Button(self.middleFrame, 
                            text = infoText['translate'],
                            bg = styles['secondaryBg'], 
                            fg = styles['secondaryFg'], 
                            activebackground = styles['additionalBg'], 
                            relief = GROOVE,
                            command = lambda: self._onBtnTranslatePress())
        self.scrollbar = Scrollbar(self.pad, 
                            orient = VERTICAL)
        self.langLabel = Label(self.pad,
                            text=infoText['chooseLang'],
                            bg = styles['secondaryFg'], 
                            fg = styles['primaryFg'],
                            borderwidth=1, 
                            relief=RIDGE,
                            highlightbackground = styles['primaryFg'],
                            highlightcolor = styles['primaryFg'],
                            font = styles['font'])
        self.langListBox = Listbox(self.pad, 
                            yscrollcommand=self.scrollbar.set,
                            bg = styles['secondaryBg'], 
                            fg = styles['secondaryFg'], 
                            selectbackground = styles['additionalBg'], 
                            selectforeground = styles['primaryFg'],
                            font = styles['font'], 
                            highlightcolor = styles['primaryFg'],
                            relief = RIDGE,
                            highlightbackground = styles['primaryFg'])

    def placeBasicVidgs(self):
        self.pad.place(x=0, y=0, relwidth=1, relheight=1)
        self.middleFrame.place(relx=0,rely=0.1,relwidth=1, relheight=0.4)
        self.entryInp.place(x=10, rely=0.1, relwidth=0.47, height=25)
        self.entryOutp.place(relx=0.5, rely=0.1, relwidth=0.48, height=25)
        self.btnTranslate.place(relx=0.0, rely=0.6, relwidth=1, relheight=0.4)
        self.langLabel.place(relx=0.598, rely=0.9, relwidth=0.37, relheight=0.1)
        self.langListBox.place(relx=0.6, rely=-1, relheight=0.35)
        self.scrollbar.config(command=self.langListBox.yview)
        self.scrollbar.place(relx=-1, rely=-1)

    def bindBasicEvents(self):
        self.root.bind_all('<KeyPress>', self._onKeyPress)
        self.entryInp.bind('<KeyPress>', lambda e: self._onEntryKeyPress(self.entryInp, e))
        self.entryOutp.bind('<KeyPress>', lambda e: self._onEntryKeyPress(self.entryOutp, e))
        self.root.bind_all('<Return>', lambda e: self._onBtnTranslatePress())
        self.root.bind_all('<Escape>', lambda e: self.escape())
        self.root.bind_all('<Button-3>', lambda e: self.changeAppLocation())
        self.btnTranslate.bind('<Enter>', lambda e: self._onBtnTranslateCover())
        self.btnTranslate.bind('<Leave>', lambda e: self._onBtnTranslateUncover())
        self.langLabel.bind('<Enter>', lambda e: self._onLangLabelCover())
        self.langLabel.bind('<Leave>', lambda e: self._onLangLabelUncover())
        self.langLabel.bind('<Button-1>', lambda e: self._onlangListBoxPress())
        
    def _onKeyPress(self, event):
        if event.state==4:
            if event.keycode==67 and not event.keysym == 'c':
                event.widget.event_generate("<<Copy>>")
            elif event.keycode==86 and not event.keysym== 'v':
                event.widget.event_generate("<<Paste>>")
            elif event.keycode==88 and not event.keysym == 'x':
                event.widget.event_generate("<<Cut>>")          
    
    def _onEntryKeyPress(self, entry, event):
        if event.state==4 and event.keycode==8:
            entry.delete(0, END)
        
    def _onBtnTranslateCover(self):
        self.btnTranslate.config(bg = CONFIG['styles']['secondaryFg'], fg = CONFIG['styles']['primaryFg'])
    def _onBtnTranslateUncover(self):
        self.btnTranslate.config(bg = CONFIG['styles']['secondaryBg'], fg = CONFIG['styles']['secondaryFg'])
        
    def _onLangLabelCover(self):
        if not self.isExpandedMore:
            self.langLabel.config(bg = CONFIG['styles']['secondaryBg'], fg = CONFIG['styles']['secondaryFg'])
        else: 
            self.langLabel.config(bg = CONFIG['styles']['secondaryFg'], fg = CONFIG['styles']['primaryFg'])
    def _onLangLabelUncover(self):
        if not self.isExpandedMore:
            self.langLabel.config(bg = CONFIG['styles']['secondaryFg'], fg = CONFIG['styles']['primaryFg'])
        else:
            self.langLabel.config(bg = CONFIG['styles']['secondaryBg'], fg = CONFIG['styles']['secondaryFg'])

    def _onBtnTranslatePress(self):
        srcText = self.entryInp.get()
        if len(srcText) == 0:
            return
        self.entryOutp.delete(0, END)
        destText =  self.doTranslate(srcText)
        self.entryOutp.insert(0, destText)
        self.makeRecordToHistoryFile(srcText, destText)

    def _onlangListBoxPress(self):
        if not self.isExpandedMore:
            self.showLangListBox()
        else:
            self.hideLangListBox()
    
    def fillLangListBox(self, topLangs = ['russian', 'english']):
        for i in topLangs:
            self.langListBox.insert(END, i)
        for i in self.translator.getAllLanguages():
            self.langListBox.insert(END,i)
        
    def showLangListBox(self):
        self.langLabel.config(
            bg = CONFIG['styles']['secondaryBg'],
            fg = CONFIG['styles']['secondaryFg'])
        self.langLabel.place(rely=0.55)
        self.langListBox.place(rely=0.65)
        self.isExpandedMore = not self.isExpandedMore
        
    def hideLangListBox(self):
        self.langLabel.config(
            bg = CONFIG['styles']['additionalBg'],
            fg = CONFIG['styles']['primaryFg'])
        self.langLabel.place(rely=0.9)
        self.langListBox.place(rely=-1)   
        self.isExpandedMore = not self.isExpandedMore

    def doTranslate(self, text):
        try:
            destLang = self.langListBox.get(ACTIVE)
        except:
            print('Language is not selected')
            destLang = 'ru'
        srcLang = self.translator.detect(text)
        try:
            result = self.translator.translate(text, srcLang, destLang)
        except Exception as e:
            result = e
        return result
        
    def makeRecordToHistoryFile(self, srcText, destText):
        historyWriter = open(CONFIG['paths']['historyFile'], "a")
        historyWriter.write('{0}\t{1}\n'.format(srcText, destText))
        historyWriter.close()

    def changeAppLocation(self):
        if self.isAppCanChangeLocation:
            root.overrideredirect(1)
            self.writeCoordsToFile()
        else:
            root.overrideredirect(0)
        self.isAppCanChangeLocation = not self.isAppCanChangeLocation

    def writeCoordsToFile(self):
        CONFIG['root']['position'] = "{0}+{1}".format(str(root.winfo_rootx()), str(root.winfo_rooty()))
        with open('.\config\config.txt', 'w') as f:
            json.dump(CONFIG, f, sort_keys=True, indent=4, ensure_ascii=False)

    def escape(self):
        if not self.isExpandedMore:
            sys.exit()
        else:
            self.hideLangListBox()

if __name__ == '__main__':
    try:
        with open(".\config\config.txt", "r") as read_file:
            CONFIG = json.load(read_file)
    except:
        print('Error occured in load config file. Bye!')
        sys.exit()

    root = Tk()
    app = Application(root)
    root.mainloop()
