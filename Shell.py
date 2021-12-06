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
import speedtest
import wikipedia as wiki


def SpeedTest():
    test = speedtest.Speedtest()
    print("Performing download test...")
    download_perform = test.download()
    print("Performing upload test...")
    upload_perform = test.upload()
    ping_perform = test.results.ping
    
    print(f"Download speed: {download_perform /1024 / 1024:.2f} Mbit/s")
    print(f"Upload speed: {upload_perform /1024 / 1024:.2f} Mbit/s")
    print(f"Ping: {ping_perform:.2f} ms")
    
def Calendar():
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

def Wikipedia():
    search_input = input("What do you want to search in Wikipedia?")
   
    if len(search_input) > 0:
       try:
            info = wiki.summary(search_input)
            print(info)
       except:
           print("I can not find a result...")
    else:
        print("I can not find a result...")


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
         Calendar()
    elif  text == "NetSpeed.pro":
          SpeedTest()
    elif text == "Wikipedia.pro":
        Wikipedia()
    else:
        txt = text.lower()
        if txt == "handrecognition" or txt == "hand recognition" or  txt == "handrecognition.pro" or txt == "hand recognition.pro" or txt == "handrecognition." :
            print("True syntax is ----> HandRecognition.pro")
        elif txt == "calendar" or txt == "calendar.":
            print("True syntax is ----> Calendar.pro")
        elif txt == "netspeed" or txt == "net speed" or  txt == "netspeed.pro" or txt == "net speed.pro" or txt == "netspeed." :
            print("True syntax is ----> NetSpeed.pro")
        elif txt == "wikipedia" or txt == "wikipedia.":
            print("True syntax is ----> Wikipedia.pro")
      
        else:
            result,error = Prometheum.run('<stdio>',text)
            if error:
               print(error.error_message())
            elif result:
               print(result)
    
    
    
 
    
    
    
     
