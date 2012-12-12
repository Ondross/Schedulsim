
from Tkinter import *
class MainWindow(Frame):
    def __init__(self,Master=None,**kw):
        kw['takefocus'] = 1


        apply(Frame.__init__,(self,Master),kw)
        self.__Frame16 = Frame(self)
        self.__Frame16.pack(side='top')
        self.__Label1 = Label(self.__Frame16,text='Scheduling Policy')
        self.__Label1.pack(side='left')
        self.__Frame2 = Frame(self,relief='raised')
        self.__Frame2.pack(anchor='n',fill='both',pady=5,side='top')
        self.__Entry2 = Entry(self.__Frame2)
        self.__Entry2.pack(side='top')
        self.__Frame1 = Frame(self)
        self.__Frame1.pack(expand='yes',fill='both',side='top')
        self.__Label2 = Label(self.__Frame1,text='Simulation')
        self.__Label2.pack(side='left')
        self.__Frame12 = Frame(self)
        self.__Frame12.pack(side='top')
        self.__Frame3 = Frame(self)
        self.__Frame3.pack(side='top')
        self.__Frame13 = Frame(self.__Frame12)
        self.__Frame13.pack(side='left')
        self.__Entry1 = Entry(self.__Frame13)
        self.__Entry1.pack(side='bottom')
        self.__Frame15 = Frame(self.__Frame12)
        self.__Frame15.pack(side='left')
        self.__Button1 = Button(self.__Frame15,text='Add Process')
        self.__Button1.pack(side='top')
        self.__Frame4 = Frame(self.__Frame3)
        self.__Frame4.pack(anchor='n',side='left')
        self.__Label3 = Label(self.__Frame4,text='Disk Wait Queue')
        self.__Label3.pack(side='top')
        self.__Listbox2 = Listbox(self.__Frame4)
        self.__Listbox2.pack(side='top')
        self.__Frame6 = Frame(self.__Frame3)
        self.__Frame6.pack(anchor='n',side='left')
        self.__Label4 = Label(self.__Frame6,text='User Imput Wait Queue')
        self.__Label4.pack(side='top')
        self.__Listbox3 = Listbox(self.__Frame6)
        self.__Listbox3.pack(side='top')
        self.__Frame7 = Frame(self.__Frame3)
        self.__Frame7.pack(side='left')
        self.__Label5 = Label(self.__Frame7,text='Run Queue')
        self.__Label5.pack(side='top')
        self.__Listbox4 = Listbox(self.__Frame7)
        self.__Listbox4.pack(side='top')
        self.__Frame5 = Frame(self.__Frame3)
        self.__Frame5.pack(side='left')
        self.__Frame8 = Frame(self.__Frame5)
        self.__Frame8.pack(side='top')
        self.__Label6 = Label(self.__Frame8,text='Running')
        self.__Label6.pack(side='top')
        self.__Listbox5 = Listbox(self.__Frame8,height=2)
        self.__Listbox5.pack(side='top')
        self.__Frame9 = Frame(self.__Frame5)
        self.__Frame9.pack(side='top')
        self.__Frame11 = Frame(self.__Frame9)
        self.__Frame11.pack(side='left')
        self.__Button2 = Button(self.__Frame11,text='Play')
        self.__Button2.pack(side='top')
        self.__Label7 = Label(self.__Frame11,text='t = 0')
        self.__Label7.pack(side='bottom')
        self.__Button3 = Button(self.__Frame11,text='Step')
        self.__Button3.pack(side='bottom')
        self.__Frame10 = Frame(self.__Frame9)
        self.__Frame10.pack(side='left')

import os.path
import sys
import time

if __name__ == '__main__':

    Root = Tk()
    App = MainWindow(Root)
    App.pack(expand='yes',fill='both')

    Root.geometry('200x280+10+10')
    Root.title('Schedulsim')
    Root.mainloop()
        