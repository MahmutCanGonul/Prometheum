# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 12:33:44 2021

@author: Mahmut Can Gonol
"""

from PIL import Image
import random
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import datetime
import webbrowser
 
def AzureGenerateContainer():
    try:
       print("Azure Blob Storage v"+__version__)
       connect_str = 'DefaultEndpointsProtocol=https;AccountName=yuklekalsinwest;AccountKey=0Ye0QQhAWmVB4PGzvr8Xg2ZzWK+oXQ004NfMHWbfdUGLoIOxDdJlZIoZaSYVCkUq9mUwrv2KhKalyFUvPj97/g==;EndpointSuffix=core.windows.net'
       blob_service_client = BlobServiceClient.from_connection_string(connect_str)
       
       # Create a unique name for the container
       container_name = str(uuid.uuid4())
       if container_name:
           container_client = blob_service_client.create_container(container_name,public_access='blob')
           print("!!!Don't forget this Name: "+container_name)
           BlobProperties(container_client,blob_service_client,container_name)  
            

    except Exception as ex:
       print('Exception:')
       print(f"AZURE Connect Error --> {ex}")

def AzureGetContanier(container_name):
    try:
       print("Azure Blob Storage v"+__version__)
       connect_str = 'DefaultEndpointsProtocol=https;AccountName=yuklekalsinwest;AccountKey=0Ye0QQhAWmVB4PGzvr8Xg2ZzWK+oXQ004NfMHWbfdUGLoIOxDdJlZIoZaSYVCkUq9mUwrv2KhKalyFUvPj97/g==;EndpointSuffix=core.windows.net'
       blob_service_client = BlobServiceClient.from_connection_string(connect_str)
       is_foundContainer=False
       # Create a unique name for the container
       if container_name:
            containers = blob_service_client.list_containers()
            
            for i in containers:
                if i.name == container_name:
                     is_foundContainer=True
                     
            if is_foundContainer:
                print(f"AZURE Container --> {container_name}")
                container_client = blob_service_client.get_container_client(container_name)
                BlobProperties(container_client,blob_service_client,container_name) 
                
            else:
                print("AZURE Container --> Not Found")
    except Exception as ex:
       print('Exception:')
       print(f"AZURE Connect Error --> {ex}")
    
def BlobProperties(container_client,blob_service_client,container_name):
    blob_list = container_client.list_blobs()
    is_empty=True
    for i in blob_list:
        print(f"{i.name}\n")
        is_empty=False
    if is_empty:
        print("Container --> Empty")
    
    print("'1' --> Upload Blob")
    print("'2' --> Download Blob")
    choice = input("Enter a Choice: ")
    
    if choice == "1":
        file_path = input("Enter a File Path for sending to Azure Blob: ")
        if file_path:
            local_file_name = []
            local_file_name = os.path.split(file_path)
            print(local_file_name[len(local_file_name)-1])
            blob_client = blob_service_client.get_blob_client(container=container_name,blob=local_file_name[len(local_file_name)-1])
            with open(file_path,'rb') as data:
                result = blob_client.upload_blob(data)
            if result:
               time=datetime.datetime.now()
               print("File Sending --> Success")
               print(f"Time --> {time}")
               print(f"Data --> {result}")    
                
    elif choice == "2":
        if is_empty == False:
            file_name = input(f"Enter a Blob Name for Downloading: ")
            is_file=False
            for i in blob_list:
                if i==file_name:
                    is_file=True
            if is_file:
                blob_client = blob_service_client.get_blob_client(container=container_name,blob=file_name)
                data = blob_client.url
                webbrowser.open(str(data))
                time=datetime.datetime.now()
                print("File Downloading --> Success")
                print(f"Time --> {time}")
                print(f"Data --> {data}")
            else:
                print("File Name is Incorrect!")
        else:
            print("You Should Upload Blob!")
            
def RemoveBlob(container_name):
    try:
       print("Azure Blob Storage v"+__version__)
       connect_str = 'DefaultEndpointsProtocol=https;AccountName=yuklekalsinwest;AccountKey=0Ye0QQhAWmVB4PGzvr8Xg2ZzWK+oXQ004NfMHWbfdUGLoIOxDdJlZIoZaSYVCkUq9mUwrv2KhKalyFUvPj97/g==;EndpointSuffix=core.windows.net'
       blob_service_client = BlobServiceClient.from_connection_string(connect_str)
       is_foundContainer=False
       # Create a unique name for the container
       if container_name:
            containers = blob_service_client.list_containers()
            
            for i in containers:
                if i.name == container_name:
                     is_foundContainer=True
            if is_foundContainer:
                choice = input("Do you really delete a container type -->  Y/N")
                if choice == "Y":
                    container_client = blob_service_client.get_container_client(container_name)
                    container_client.delete_container()
                    print(f"{container_name} --> Removed")
            else:
                print("Container Name is --> False")
        
    except Exception as ex:
       print('Exception:')
       print(f"AZURE Connect Error --> {ex}")
        
    

def AzureBlob():
    print("'1' --> Generate New Container")
    print("'2' --> Get Container")
    print("'3' --> Remove Container")
    print("'exit' --> Exit the Platfrom")
    while True:
        choice = input("Please Enter a Choice: ")
        if choice == "exit":
            break
        elif choice == "1":
            AzureGenerateContainer()
        elif choice == "2":
            container_name = input("Please Enter a Container Name: ")
            AzureGetContanier(container_name)
        elif choice == 3:
            container_name = input("Please Enter a Container Name: ")
            RemoveBlob(container_name)
        else:
            print("Invalid Commits!")
    
     
AzureBlob()     

      

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
        













