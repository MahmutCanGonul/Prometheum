# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 14:13:07 2021

@author: Mahmut Can Gonol
"""
import Prometheum
import datetime
import HandRecognition
import platform
import os
import tkinter
import calendar

while True:
    text = input("prometheum => ")
    if text == "exit":
        break
    elif text == "time":
        print(datetime.datetime.now())
    elif text == "time.year":
        time_now = datetime.datetime.now()
        print(time_now.year)
    elif text == "time.day":
        time_now = datetime.datetime.now()
        print(time_now.day)
    elif text == "HandRecognition.pro":
        print("If you want exit please enter 'q' ")
        HandRecognition.main()
    elif text == "system":
         print(platform.platform())      
    elif text == "system.info":
        print(platform.uname())
    elif text == "clear":
        os.system('cls')
    elif text == "Calendar.pro":
        year_input = input("Enter a year please: ") 
        if  year_input.isdigit():
            gui = tkinter.Tk()
            gui.config(background='grey')
            gui.title("Calender for the year")
            gui.geometry("550x600")
            year = int(year_input)
            gui_content= calendar.calendar(year)
            calYear = tkinter.Label(gui, text= gui_content, font= "Consolas 10 bold")
            calYear.grid(row=5, column=1,padx=20)
            gui.mainloop()
        else:
            print("Year is not valid!")
        
    else:
        txt = text.lower()
        if txt == "handrecognition" or txt == "hand recognition" or  txt == "handrecognition.pro" or txt == "hand recognition.pro" or txt == "handrecognition." :
            print("True syntax is ----> HandRecognition.pro")
        elif txt == "calendar" or txt == "calendar.":
            print("True syntax is ----> Calendar.pro")
        else:
            result,error = Prometheum.run('<stdio>',text)
            if error:
               print(error.error_message())
            elif result:
               print(result)
    
    
    
 
     
