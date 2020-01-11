# -*- coding: utf-8 -*-
import AppInfo
import myYandex
from tkinter import *
from PIL import Image as Image
import PIL.ImageTk as ImageTk
from tkinter import simpledialog
from tkinter import messagebox
import os

class Application(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        root.bind_all("<Return>", lambda e: self.btnTranslPress())
        root.bind_all("<Escape>", lambda e: self.Escape())
        root.bind_all("<Button-3>", lambda e: self.ChangeAppLocat())
        root.bind_all("<Key>", self._onKeyRelease, "+")
        
        self.isCanChangeAppLocat= False
        
        self.CreateBasicVidgs()
        self.PlaceBasicVidgs()
   
    def CreateBasicVidgs(self):
        self.pad = Canvas(root)
        self.bgImage = ImageTk.PhotoImage(Image.open(AppInfo.PATHs['bgImg']))
        self.imagesprite = self.pad.create_image(0,0, image=self.bgImage)

        self.middleFrame = Frame(self.pad, bg="#cccc00", highlightbackground="#654321", 
                                highlightcolor="#654321", highlightthickness=1)

        self.btnTranslate = Button(self.middleFrame, text=AppInfo.text['btn'][0], fg="#e29246", bg="#654321", relief = GROOVE, 
                            activebackground = "#e29246", command = lambda: self.btnTranslPress())
        self.btnTranslate.bind("<Enter>", lambda e: self.btnTranslConver())
        self.btnTranslate.bind("<Leave>", lambda e: self.btnTranslUncover())
        
        self.btnHow = Button(self.middleFrame, text=AppInfo.text['btn'][1], fg="#e29246", bg="#654321", relief = GROOVE, 
                            activebackground = "#e29246", command = lambda: self.FAQ())
        self.btnHow.bind("<Enter>", lambda e: self.btnHowCover())
        self.btnHow.bind("<Leave>", lambda e: self.btnHowUncover())
        self.btnHow.bind("<Return>", lambda e: self.FAQ())
        
        self.entryInp = Entry( self.middleFrame, validate="focusin", bg = "#fbec5d",
                            fg = "#654321", font = "Helvetica")
        self.entryOutp = Entry(self.middleFrame, bg = "#fbec5d",
                            fg = "#654321", font = "Helvetica")
        
        self.entryInp.bind("<Control_L>", lambda e: self.DelInpTxt())
        
    def PlaceBasicVidgs(self):
        self.pad.place(x=0, y=0, relwidth=1, relheight=1)
        self.middleFrame.place(relx=0,rely=0.3,relwidth=1, relheight=0.4)
        self.btnTranslate.place(relx=0.0, rely=0.6, relwidth=0.93, relheight=0.4)
        self.btnHow.place(relx=0.931, rely=0.6, relwidth=0.07, relheight=0.4)
        self.entryInp.place(x = 10, rely = 0.1, relwidth = 0.47, height = 25)
        self.entryOutp.place(relx = 0.5, rely = 0.1, relwidth = 0.48, height = 25)
        
    def _onKeyRelease(self,event):
        ctrl  = (event.state & 0x4) != 0
        if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
            event.widget.event_generate("<<Cut>>")

        if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
            event.widget.event_generate("<<Paste>>")

        if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")    
            
    def btnTranslConver(self):
        self.btnTranslate.config(bg = "#e29246", fg = "#654321")
    def btnTranslUncover(self):
        self.btnTranslate.config(bg = "#654321", fg="#e29246")
        
    def btnHowCover(self):
        self.btnHow.config(bg = "#e29246", fg = "#654321")
    def btnHowUncover(self):
        self.btnHow.config(bg = "#654321", fg="#e29246")
    

    def btnTranslPress(self):
        text = self.entryInp.get()
        if len(text) < 1:
            return 
        self.entryOutp.delete(0, END)
        self.entryOutp.insert(0, self.DoTranslate(text))
        
    def DoTranslate(self, text):
        user = myYandex.User(AppInfo.PATHs['token'])
        return user.DoTranslate(text)
        
    def FAQ(self):
        answer = simpledialog.askstring(AppInfo.text['info']['name'],AppInfo.text['info']['FAQ'])
        if answer is None:
            return 
        elif len(answer) < 30:
            messagebox.showinfo(AppInfo.text['error']['name'],AppInfo.text['error']['token'])
            return
        else:
            if not os.path.exists(AppInfo.PATHs['api']):
                os.mkdir(AppInfo.PATHs['api'])
            if not os.path.exists(AppInfo.PATHs['token']):
                self.CreateToken(answer)
                messagebox.showinfo(AppInfo.text['info']['name'],AppInfo.text['info']['token'][2])
            else:
                check = messagebox.askquestion(AppInfo.text['info']['token'][0], AppInfo.text['info']['token'][1])
                if check == 'yes':
                    self.CreateToken(answer)
                    messagebox.showinfo(AppInfo.text['info']['name'],AppInfo.text['info']['token'][2])
            
    def CreateToken(self, token):
        writer = open(AppInfo.PATHs['token'], "w")
        writer.write(str(token).strip())
        writer.close() 
        
    def DelInpTxt(self):
        self.entryInp.delete(0, END)
        
    def Escape(self):   
        sys.exit()
        
    def ChangeAppLocat(self):
        if self.isCanChangeAppLocat:
            root.overrideredirect(1)
            self.WriteCoords()
        else:
            root.overrideredirect(0)
        self.isCanChangeAppLocat = not self.isCanChangeAppLocat
            
    def WriteCoords(self):
        writer = open(AppInfo.PATHs['position'], "w")
        writer.write("{0}+{1}".format(str(root.winfo_rootx()), str(root.winfo_rooty())))
        writer.close()
       
    
if __name__ == '__main__':        
    root = Tk()
    
    try:
        reader = open(AppInfo.PATHs['position'],'r')
        root.geometry("{0}+{1}".format(AppInfo.text['size'],reader.read()))
        reader.close()
    except:
        print(AppInfo.text['error']['position'])
        root.geometry("{0}+{1}".format(AppInfo.text['size'], '0+0'))
        
    root.title(AppInfo.text['title'])
    root.resizable(0,0)
    root.overrideredirect(1)
    
    try:
        root.iconbitmap(AppInfo.PATHs['icon'])
    except:
        print(AppInfo.text['error']['icon'])
    app = Application(root)
    root.mainloop()