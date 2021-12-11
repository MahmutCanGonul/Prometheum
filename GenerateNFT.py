# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 12:33:44 2021

@author: Mahmut Can Gonol
"""

from PIL import Image
import random
 

def GenerateNFT():
    print("Don't forget only file png")
    array = []
    nft_counts = input("Enter a how many create a NFT: ")
    count_values = input("Enter a how many different title a variable: ")
    if count_values.isdigit():
       count=0
       while True:
           value = input(f"{count}.Title Enter a image a png format: ")
           if value=="exit":
              count+=1
              array.append(str(count))
              if count >=int(count_values):
                 break
           elif value=="fullexit":
               break
           else:
               if '.png' in value:
                   array.append(value)
               else:
                 print("Error. Please enter '.png' file")

    is_empty = False    
    if len(array) == 0:
       is_empty=True

    is_error = False
    if is_empty == False:
       variables = []
       for i in range(len(array)):
           if array[i].isdigit() == False:
              variables.append(array[i])
           images = []
       for i in range(len(variables)):
           try:
              img = Image.open(variables[i]).convert('RGBA')
              img.putalpha(1)
              print(img)
              images.append(img)
           except:
              is_error = True
              print("Detect denised file!")
    
       
       if is_error==False:
          """ 
          for i in range(len(images)):
              if i!=0:
                  x,y = images[i].size
                  images[0].paste(images[i],(random.randint(0,x),random.randint(0,y)))             
          
          images[0].show()   
          """ 
          count=len(images)
          break_count=0
          
          while True:
              try:
                  count-=1
                  x,y = images[count].size
                  images[0].paste(images[count],(random.randint(0,x),random.randint(0,y)))  
              
                  if count == 0:
                     count = len(images)
                     break_count+=1
                     images[0].show()
                  if break_count == int(nft_counts):
                     break
              except:
                  print("Something get issue!")
                  break
        













