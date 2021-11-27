# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 14:13:07 2021

@author: Mahmut Can Gonol
"""

import Prometheum


while True:
    text = input("prometheum => ")
    if text == "exit":
        break
    result,error = Prometheum.run('<stdio>',text)
    
    if error:
        print(error.error_message())
    else:
        print(result)
    
