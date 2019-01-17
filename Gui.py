import os
from tkinter import *
from tkinter.messagebox import *
import pandas as pd 
import datetime
import shutil
from CustardSheet import SelectDate
from CustardSheet import Prediction
from CustardSheet import Prediction_half


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
        Button(self, text='Login', command=self.loginCheck).grid(row=3, column=4,pady=10)  
#        Button(self, text='Log out', command=self.quit).grid(row=3, column=1, stick=E)
    
    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        if name=="Manager" and secret=='andys':  
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
        self.master.title("Custard Sales Projection")
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
        self._tablePane.grid(row = 3, column = 0, pady=3)
        
        """Create Labels and entry fileds of the attributes pane"""
        self._ProjectedLabel = Label(self._attributesPane, text = "Projected Sales")
        self._ProjectedLabel.grid(row = 0, column = 0)
        self._DatesLabel = Label(self._attributesPane, text = "Dates")
        self._DatesLabel.grid(row = 1, column = 0, sticky = W)
        """Create the entry part"""
        #name entry
        self._ProjectedVar = StringVar()
        self._ProjectedEntry = Entry(self._attributesPane, textvariable = self._ProjectedVar)
        self._ProjectedEntry.grid(row = 0, column = 1)

        #city entry
        self._DatesVar = StringVar()
        self._DatesEntry = Entry(self._attributesPane, textvariable = self._DatesVar)
        self._DatesEntry.grid(row = 1, column = 1)
        
        """Create buttons"""
        #retrive all button
        self._retriveButton = Button(self._buttonsPane, text = "Report",command = self._retriveAll)
        self._retriveButton.grid(row = 0, column = 0,)
        self._retriveButton = Button(self._buttonsPane, text = "Half Hour",command = self.reprort_halfhour)
        self._retriveButton.grid(row = 0, column = 1,)
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
        self._ProjectedCol = Listbox(self._tablePane, width = 10, selectborderwidth =2, height = 27, yscrollcommand = scrollbar.set)
        self._ProjectedCol.grid(row = 0, column = 0, sticky = W+E+N+S)
        self._ProLabel = Label(self._buttonsPane, text = "HOUR").grid(row = 1, column = 0,padx=16)        
        #city column
        self._DatesCol = Listbox(self._tablePane,selectborderwidth =2, width = 10, height = 27)
        self._DatesCol.grid(row = 0, column = 1)
        self._dateLabel = Label(self._buttonsPane, text = "Vanilla (Treats)", wraplength = 50).grid(row = 1, column = 1, padx=10)
        #street column
        self._iCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 27, yscrollcommand =scrollbar.set)
        self._iCol.grid(row = 0, column = 2,sticky =W + E+ N +S)
        self._iiLabel = Label(self._buttonsPane, text = "Vanilla (ounces)", wraplength = 50).grid(row = 1, column = 2,padx=12)

        
        self._aCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 27, yscrollcommand =scrollbar.set)
        self._aCol.grid(row = 0, column = 3,sticky =W + E+ N +S)
        self._aaLabel = Label(self._buttonsPane, text = "Vanilla (Buckets)",wraplength = 50).grid(row = 1, column = 3,padx=6)

        self._bCol = Listbox(self._tablePane,selectborderwidth =2, width = 10, height = 27, yscrollcommand =scrollbar.set)
        self._bCol.grid(row = 0, column = 4,sticky =W + E+ N +S)
        self._bbLabel = Label(self._buttonsPane, text = "Chocolate (Treats)", wraplength = 60).grid(row = 1, column = 4,padx=6)
        
        self._cCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 27, yscrollcommand =scrollbar.set)
        self._cCol.grid(row = 0, column = 5,sticky =W + E+ N +S)
        self._dateLabel = Label(self._buttonsPane, text = "Chocolate (ounces)", wraplength = 60).grid(row = 1, column = 5,padx=4)
        
        self._dCol = Listbox(self._tablePane, selectborderwidth =2,width = 10, height = 27, yscrollcommand =scrollbar.set)
        self._dCol.grid(row = 0, column = 6,sticky =W + E+ N +S)
        self._ddLabel = Label(self._buttonsPane, text = "Chocolate (Buckets)", wraplength = 60).grid(row = 1, column = 6,padx=4)

        """Create button functions"""
    def yview(self,*args):
        self._ProjectedCol.yview(*args)
        self._DatesCol.yview(*args)
        self._iCol.yview(*args)
        self._aCol.yview(*args)
        self._bCol.yview(*args)
        self._cCol.yview(*args)
        self._dCol.yview(*args)

        #Retrive all button function
    def _retriveAll(self):
        UserInput =self._ProjectedVar.get()
        today =self._DatesVar.get()
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
            length =len(Report)
            print(Report)
            for i in range(length-1):
                self._ProjectedCol.insert(END, datetime.datetime.strptime(str(Report.iloc[i:i+1,0:1].values.tolist()[0][0]), "%H").strftime("%I:%M %p"))
                self._ProjectedCol.see(END)         
                self._DatesCol.insert(END, Report.iloc[i:i+1,1:2].values.tolist())
                self._DatesCol.see(END)
                self._iCol.insert(END, Report.iloc[i:i+1,2:3].values.tolist())
                self._iCol.see(END)
                self._aCol.insert(END, Report.iloc[i:i+1,3:4].values.tolist())
                self._aCol.see(END)
                self._bCol.insert(END,Report.iloc[i:i+1,4:5].values.tolist())
                self._bCol.see(END)
                self._cCol.insert(END,Report.iloc[i:i+1,5:6].values.tolist())
                self._cCol.see(END)
                self._dCol.insert(END,Report.iloc[i:i+1,6:7].values.tolist())
                self._dCol.see(END)
            self._ProjectedCol.insert(END, Report.iloc[length-1:length,0:1].values.tolist())
            self._ProjectedCol.see(END)         
            self._DatesCol.insert(END, Report.iloc[length-1:length,1:2].values.tolist())
            self._DatesCol.see(END)
            self._iCol.insert(END, Report.iloc[length-1:length,2:3].values.tolist())
            self._iCol.see(END)
            self._aCol.insert(END, Report.iloc[length-1:length,3:4].values.tolist())
            self._aCol.see(END)
            self._bCol.insert(END,Report.iloc[length-1:length,4:5].values.tolist())
            self._bCol.see(END)
            self._cCol.insert(END,Report.iloc[length-1:length,5:6].values.tolist())
            self._cCol.see(END)
            self._dCol.insert(END,Report.iloc[length-1:length,6:7].values.tolist())
            self._dCol.see(END)
            
            shutil.rmtree(output)

        #Retrive all button function
    def reprort_halfhour(self):
        UserInput =self._ProjectedVar.get()
        today =self._DatesVar.get()
        if UserInput =="":
            showerror(title="Error", message="Please input Projecred Sales")
        else:
            if today=="":
                Dates = datetime.datetime.today()
            else:
                Dates =datetime.datetime.strptime(today, '%Y-%m-%d')
            os.makedirs(output)
            SelectDate(Dates)
            Report = Prediction_half(int(UserInput))
            length =len(Report)
            print(Report)
            for i in range(length-1):
                self._ProjectedCol.insert(END, datetime.datetime.strptime(str(Report.iloc[i:i+1,0:1].values.tolist()[0][0]), "%H:%M").strftime("%I:%M %p"))
                self._ProjectedCol.see(END)         
                self._DatesCol.insert(END, Report.iloc[i:i+1,1:2].values.tolist())
                self._DatesCol.see(END)
                self._iCol.insert(END, Report.iloc[i:i+1,2:3].values.tolist())
                self._iCol.see(END)
                self._aCol.insert(END, Report.iloc[i:i+1,3:4].values.tolist())
                self._aCol.see(END)
                self._bCol.insert(END,Report.iloc[i:i+1,4:5].values.tolist())
                self._bCol.see(END)
                self._cCol.insert(END,Report.iloc[i:i+1,5:6].values.tolist())
                self._cCol.see(END)
                self._dCol.insert(END,Report.iloc[i:i+1,6:7].values.tolist())
                self._dCol.see(END)
            self._ProjectedCol.insert(END, Report.iloc[length-1:length,0:1].values.tolist())
            self._ProjectedCol.see(END)         
            self._DatesCol.insert(END, Report.iloc[length-1:length,1:2].values.tolist())
            self._DatesCol.see(END)
            self._iCol.insert(END, Report.iloc[length-1:length,2:3].values.tolist())
            self._iCol.see(END)
            self._aCol.insert(END, Report.iloc[length-1:length,3:4].values.tolist())
            self._aCol.see(END)
            self._bCol.insert(END,Report.iloc[length-1:length,4:5].values.tolist())
            self._bCol.see(END)
            self._cCol.insert(END,Report.iloc[length-1:length,5:6].values.tolist())
            self._cCol.see(END)
            self._dCol.insert(END,Report.iloc[length-1:length,6:7].values.tolist())
            self._dCol.see(END)
            
            shutil.rmtree(output)
        
                
    #clear table button function
    def _clearTable(self):
        self._ProjectedCol.delete(0 , END)
        self._DatesCol.delete(0 , END)
        self._iCol.delete(0 , END)
        self._aCol.delete(0 , END)
        self._bCol.delete(0 , END)
        self._cCol.delete(0 , END)
        self._dCol.delete(0 , END)

    #clear entry button function
    def _clearEntry(self):
        self._ProjectedVar.set("")
        self._DatesVar.set("")



