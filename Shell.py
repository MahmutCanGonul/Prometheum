# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 14:13:07 2021

@author: Mahmut Can Gonol
"""
import Prometheum
import datetime
while True:
    text = input("prometheum => ")
    if text == "cikis":
        break
    elif text == "zaman":
        print(datetime.datetime.now())
    elif text == "zaman.yil":
        time_now = datetime.datetime.now()
        print(time_now.year)
    elif text == "zaman.gun":
        time_now = datetime.datetime.now()
        print(time_now.day)
    else:
        result,error = Prometheum.run('<stdio>',text)
        if error:
            print(error.error_message())
        elif result:
            print(result)
    
    
    
    
