import os
from tkinter import *
from tkinter.messagebox import *
import pandas as pd 
import datetime
import shutil
from CustardSheet import SelectDate
from CustardSheet import Prediction

currentpath = os.getcwd()
output =currentpath+"\\Output"

class LoginPage(Frame):  
    def __init__(self):
        super().__init__()
        self.username = StringVar()  
        self.password = StringVar()
        self.pack()
        self.createForm() 
    def createForm(self):
        Label(self).grid(row=0, stick=W, pady=10)  
        Label(self, text = 'Your ID: ').grid(row=1, stick=W, pady=10)  
        Entry(self, textvariable=self.username).grid(row=1, column=1, stick=E)  
        Label(self, text = 'Password: ').grid(row=2, stick=W, pady=10)  
        Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick=E)  
        Button(self, text='Login', command=self.loginCheck).grid(row=3, stick=W, pady=10)  
        Button(self, text='Log out', command=self.quit).grid(row=3, column=1, stick=E)
    
    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        if name=="123" and secret=='123':  
            self.destroy()
            #page2 = DatabaseInterface()
            DatabaseInterface().mainloop()
            
        else:  
            showinfo(title='error', message='Your ID or password is not correct！')  
            # print('wrong ID or Password')
           
class DatabaseInterface (Frame):    
    
    def __init__(self):
        """Set up the window"""
        Frame.__init__(self)
        self.master.title("CustardSheet Daily Report")
        self.grid()

        """Create the nested panes"""
        #attributes pane
        self._attributesPane = Frame(self)
        self._attributesPane.grid(row = 0, column = 0, sticky = W)
        
        #button pane
        self._buttonsPane = Frame(self)
        self._buttonsPane.grid(row = 1, column = 0, sticky = W+E)

        #table pane
        self._tablePane = Frame(self)
        self._tablePane.grid(row = 2, column = 0, pady=5)
        
        """Create Labels and entry fileds of the attributes pane"""
        self._nameLabel = Label(self._attributesPane, text = "Projected Sales")
        self._nameLabel.grid(row = 0, column = 0)
        self._cityLabel = Label(self._attributesPane, text = "Dates")
        self._cityLabel.grid(row = 1, column = 0, sticky = W)
        """Create the entry part"""
        #name entry
        self._nameVar = StringVar()
        self._nameEntry = Entry(self._attributesPane, textvariable = self._nameVar)
        self._nameEntry.grid(row = 0, column = 1)

        #city entry
        self._cityVar = StringVar()
        self._cityEntry = Entry(self._attributesPane, textvariable = self._cityVar)
        self._cityEntry.grid(row = 1, column = 1)
        
        """Create buttons"""
        #retrive all button
        self._retriveButton = Button(self._buttonsPane, text = "Report",command = self._retriveAll)
        self._retriveButton.grid(row = 0, column = 0,)
      
        #clear table button
        self._clearTableButton = Button(self._buttonsPane, text = "Clear Data",
                                        command = self._clearTable)
        self._clearTableButton.grid(row = 0, column = 3)
        
        #clear entry button
        self._clearEntryButton = Button(self._buttonsPane, text = "Clear Entry",
                                        command = self._clearEntry)
        self._clearEntryButton.grid(row = 0, column = 4)

        #scrollbar
        scrollbar = Scrollbar(self._tablePane, orient =VERTICAL, command =self.yview)
        scrollbar.grid(row = 0, column =3, sticky = N+S)
        
        """Create table"""
        #name column
        self._nameCol = Listbox(self._tablePane, width = 5, selectborderwidth =2, height = 15, yscrollcommand = scrollbar.set)
        self._nameCol.grid(row = 0, column = 0, sticky = W+E+N+S)
        self._nnLabel = Label(self._buttonsPane, text = "HOUR").grid(row = 1, column = 0)        
        #city column
        self._cityCol = Listbox(self._tablePane,selectborderwidth =2, width = 10, height = 15)
        self._cityCol.grid(row = 0, column = 1)
        self._ccLabel = Label(self._buttonsPane, text = "Treats_V").grid(row = 1, column = 1, padx=3)
        #street column
        self._streetCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 15, yscrollcommand =scrollbar.set)
        self._streetCol.grid(row = 0, column = 2,sticky =W + E+ N +S)
        self._ssLabel = Label(self._buttonsPane, text = "OUNCES_V").grid(row = 1, column = 2,padx=7)

        
        self._aCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 15, yscrollcommand =scrollbar.set)
        self._aCol.grid(row = 0, column = 3,sticky =W + E+ N +S)
        self._aaLabel = Label(self._buttonsPane, text = "Buckets_V").grid(row = 1, column = 3,padx=5)

        self._bCol = Listbox(self._tablePane,selectborderwidth =2, width = 10, height = 15, yscrollcommand =scrollbar.set)
        self._bCol.grid(row = 0, column = 4,sticky =W + E+ N +S)
        self._bbLabel = Label(self._buttonsPane, text = "Treats_C").grid(row = 1, column = 4,padx=3)
        
        self._cCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 15, yscrollcommand =scrollbar.set)
        self._cCol.grid(row = 0, column = 5,sticky =W + E+ N +S)
        self._CCLabel = Label(self._buttonsPane, text = "OUNCES_C").grid(row = 1, column = 5,padx=5)
        
        self._dCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 15, yscrollcommand =scrollbar.set)
        self._dCol.grid(row = 0, column = 6,sticky =W + E+ N +S)
        self._ddLabel = Label(self._buttonsPane, text = "Buckets_C").grid(row = 1, column = 6,padx=5)

        """Create button functions"""
    def yview(self,*args):
        self._nameCol.yview(*args)
        self._cityCol.yview(*args)
        self._streetCol.yview(*args)
        self._aCol.yview(*args)
        self._bCol.yview(*args)
        self._cCol.yview(*args)
        self._dCol.yview(*args)

        #Retrive all button function
    def _retriveAll(self):
        UserInput =self._nameVar.get()
        today =self._cityVar.get()
        if UserInput =="":
            showerror(title="Error", message="Please input Projecred Sales")
        else:
            if today=="":
                Dates = datetime.datetime.today()
            else:
                Dates =datetime.datetime.strptime(today, '%Y-%m-%d')
            os.makedirs(output)
            SelectDate(Dates)
            Report = Prediction(int(UserInput))
            print(Report)
            for i in range(len(Report)):
                self._nameCol.insert(END, Report.iloc[i:i+1,0:1].values.tolist())
                self._nameCol.see(END)         
                self._cityCol.insert(END, Report.iloc[i:i+1,1:2].values.tolist())
                self._cityCol.see(END)
                self._streetCol.insert(END, Report.iloc[i:i+1,2:3].values.tolist())
                self._streetCol.see(END)
                self._aCol.insert(END, Report.iloc[i:i+1,3:4].values.tolist())
                self._aCol.see(END)
                self._bCol.insert(END,Report.iloc[i:i+1,4:5].values.tolist())
                self._bCol.see(END)
                self._cCol.insert(END,Report.iloc[i:i+1,5:6].values.tolist())
                self._cCol.see(END)
                self._dCol.insert(END,Report.iloc[i:i+1,6:7].values.tolist())
                self._dCol.see(END)
            shutil.rmtree(output)
                
    #clear table button function
    def _clearTable(self):
        self._nameCol.delete(0 , END)
        self._cityCol.delete(0 , END)
        self._streetCol.delete(0 , END)
        self._aCol.delete(0 , END)
        self._bCol.delete(0 , END)
        self._cCol.delete(0 , END)
        self._dCol.delete(0 , END)

    #clear entry button function
    def _clearEntry(self):
        self._nameVar.set("")
        self._cityVar.set("")



