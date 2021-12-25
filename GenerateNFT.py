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
import requests

 

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
    print("->BLOBS<-")
    count=0
    for i in blob_list:
        count+=1
        print(f"{count}-->{i.name}\n")
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
                choice = input("Do you really delete a container type --> Y/N")
                if 'Y' in choice:
                    container_client = blob_service_client.get_container_client(container_name)
                    container_client.delete_container()
                    print(f"{container_name} --> Removed")
            else:
                print("Container Name is --> False")
        
    except Exception as ex:
       print('Exception:')
       print(f"AZURE Connect Error --> {ex}")
        
    

def AzureBlob():
    while True:
        print("///////////////////////////////////")
        print("'1' --> Generate New Container")
        print("'2' --> Get Container")
        print("'3' --> Remove Container")
        print("'exit' --> Exit the Platfrom")
        print("///////////////////////////////////")
        
        choice = input("Please Enter a Choice: ")
        if choice == "exit":
            break
        elif choice == "1":
            AzureGenerateContainer()
        elif choice == "2":
            container_name = input("Please Enter a Container Name: ")
            AzureGetContanier(container_name)
        elif choice == "3":
            container_name = input("Please Enter a Container Name: ")
            RemoveBlob(container_name)
        else:
            print("Invalid Commits!")
    

def AzureImageAnalysis():
    path = input("Enter a URL For Analysis: ")
    try: 
       url = "https://microsoft-computer-vision3.p.rapidapi.com/analyze"
       querystring = {"language":"en","descriptionExclude":"Celebrities","visualFeatures":"ImageType","details":"Celebrities"}
       payload = "{\r\"url\": \""+path+"\"\r}"
       headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "microsoft-computer-vision3.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }
       response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
       print("Azure Computer Vision --> Success")
       print(response.json())
    except Exception as ex:
        print(f"Azure Computer Vision Error --> {ex}")

def AzureDescribeAnalysis():
     path = input("Enter a URL For Analysis: ")
     try:
         url = "https://microsoft-computer-vision3.p.rapidapi.com/describe"

         querystring = {"language":"en","maxCandidates":"1","descriptionExclude":"Celebrities"}

         payload = "{\r\n    \"url\": \""+path+"\"\r\n}"
         headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "microsoft-computer-vision3.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }

         response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
         print("Azure Computer Vision --> Success")
         print(response.json())
    
     except Exception as ex:
        print(f"Azure Computer Vision Error --> {ex}")    

def AzureOCR():
    path = input("Enter a URL For Analysis: ")
    try: 
        url = "https://microsoft-computer-vision3.p.rapidapi.com/detect"

        payload = "{\r\n    \"url\": \""+path+"\"\r\n}"
        headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "microsoft-computer-vision3.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }

        response = requests.request("POST", url, data=payload, headers=headers)
        print("Azure Computer Vision --> Success")
        print(response.json())
    except Exception as ex:
        print(f"Azure Computer Vision Error --> {ex}")    

def AzureTextAI():
     
     text = input("Enter a Sentence or Paragraph for text analsysis: ")
     data = []
     sending_text = ""
     
     if text:
         data = text.split(' ')
         if len(data) > 0:
             for i in range(len(data)):
                 sending_text += data[i]
         else:
             sending_text = text
         try:
             
            url = "https://microsoft-content-moderator2.p.rapidapi.com/ProcessText/Screen"
            querystring = {"PII":"true","autocorrect":"true","classify":"true"}

            payload = text
            headers = {
    'content-type': "text/plain",
    'x-rapidapi-host': "microsoft-content-moderator2.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            print("Azure Computer Vision --> Success")
            print(response.json()['PII'])
         except Exception as ex:
            no_pii = f"{ex}"
            if 'PII' in no_pii:
                print("Azure Computer Vision --> No 'PII' Data")
            else:
                print(f"Azure Computer Vision Error --> {no_pii}")  
            

def AzureFaceAI():
    count=0
    total_age=0
    male_count=0
    female_count=0
    total_smile=0
    url_path = input("Enter a URL For Analysis: ")
    if url_path:
        try:
            url = "https://microsoft-face1.p.rapidapi.com/detect"

            querystring = {"returnFaceAttributes":"age, gender,headPose,smile,facialHair,glasses,emotion","detectionModel":"detection_01","returnFaceLandmarks":"true","recognitionModel":"recognition_01","returnFaceId":"true","returnRecognitionModel":"true"}
     
            payload = "{\r\"url\": \""+url_path+"\"\r}"
            headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "microsoft-face1.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            result = response.json()
            
            if len(result) >1:
                print(f"Detected People Number --> {len(result)}")
                for i in range(len(result)):
                    count=i+1
                    data = result[i]
                    face_attributes = data['faceAttributes']
                    total_age +=face_attributes['age']
                    print(f"{count}.Age-> {face_attributes['age']}")
                    if face_attributes['gender'] == "male":
                        male_count+=1
                    elif face_attributes['gender'] == "female":
                        female_count+=1
                    
                    total_smile+=face_attributes['smile']
                    
                    
                average = total_age / len(result)
                average_smile = total_smile / len(result)
                print(f"Total Age Average --> {average}")
                print(f"Total Smile Average --> 1/{average_smile}")
                print(f"Male Number --> {male_count}")
                print(f"Female Number --> {female_count}")
                
            else:
                data = result[0]
                face_attributes = data['faceAttributes']
                emotion = face_attributes['emotion']
                emotions = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
                
                faceid = data['faceId']
                age = face_attributes['age']
                gender = face_attributes['gender']
                glasses = face_attributes['glasses']
                
                print(f"FACE ID --> {faceid}")
                print(f"AGE --> {age}")
                print(f"GENDER --> {gender}")
                print(f"GLASSES --> {glasses}")
                points = []
                for i in range(len(emotions)):
                    subje = emotions[i].upper()
                    result = emotion[emotions[i]]
                    points.append(result)
                    print(f"{subje} --> 1/{result}")
                points.sort()
                for i in range(len(emotions)):
                    subje = emotions[i].upper()
                    result = emotion[emotions[i]]
                    if result == points[len(points)-1]:
                        print(f"DETECTED EMOTION --> {subje} --> 1/{result}")
                    
                    
                
                
                
        except Exception as ex:
            print(f"Azure Computer Vision Error --> {ex}")
    



def TranslateAI():
    languages = ["English","Spanish","Franche","German","Turkish","Chinese","Japanese","Arabic","Hebrew","Russian","Portuguese"]
    keys = {languages[0]:"en",languages[1]:"es",languages[2]:"fr",languages[3]:"de",
            languages[4]:"tr",languages[5]:"zh-cn",languages[6]:"jp",languages[7]:"ar",languages[8]:"he",languages[9]:"ru",languages[10]:"pt"}
    target_lan = ""
    
    for i in range(len(languages)):
        print(f"'{i+1}' --> {languages[i]}")
    
    choice = input("Which language to translate? ")
    
    if choice == "1":
        target_lan=keys[languages[int(choice)-1]]
    elif choice == "2":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "3":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "4":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "5":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "6":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "7":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "8":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "9":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "10":
         target_lan=keys[languages[int(choice)-1]]
    elif choice == "11":
         target_lan=keys[languages[int(choice)-1]]
         
    else:
        return "Choice --> Not Correct"
    
    
    sentence = input("Enter a Sentence: ")
    if sentence:
        try:
            url = "https://microsoft-translator-text.p.rapidapi.com/translate"
            querystring = {"to":target_lan,"api-version":"3.0","profanityAction":"NoAction","textType":"plain"}
            payload = "[\r\n    {\r\n        \"Text\": \""+sentence+"\"\r\n    }\r\n]"
            headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "microsoft-translator-text.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }

            response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            data = response.json()
            result = data[0]['translations']
            print(f"json --> {result}")
            print(f"Result Sentence --> {result[0]['text']}")
        except Exception as ex:
            print(f"Error --> {ex}")
            

def AzureBingSearch():
    search = input("What do you want search?")
    if search:
        try:
           url = "https://bing-news-search1.p.rapidapi.com/news/search"

           querystring = {"q":search,"mkt":"en-US","freshness":"Day","textFormat":"Raw","safeSearch":"Off"}

           headers = {
    'x-bingapis-sdk': "true",
    'x-rapidapi-host': "bing-news-search1.p.rapidapi.com",
    'x-rapidapi-key': "843406cdb2msh623e555d8416d8ep1d7e8ajsnb9afd7d794c4"
    }
 
           response = requests.request("GET", url, headers=headers, params=querystring)
           json = response.json()
           values = json['value']
           counts = []
           url = []
           
           for i in range(len(values)):
               value = values[i]
               print(f"Article --> '{i+1}'")
               print(f"Subject --> {value['name']}")
               print(f"URL --> {value['url']}")
               print(f"Description --> {value['description']}")
               print(f"Publish Date --> {value['datePublished']}")
               counts.append(i+1)
               url.append(value['url'])
               print("//////////////////////")
               print()
           choice = input("Which news do you want to search on Network Engine?")
           if choice.isdigit():
               ch = int(choice)
               for i in range(len(counts)):
                   if counts[i] == ch:
                       webbrowser.open(url[ch-1])
                       break
                  
        except Exception as ex:
            print(f"Error --> {ex}")

 



def GenerateNFT():
    print("Don't forget only file png")
    print("'exit' --> See the result")
    array = []
    nft_counts = input("Enter a how many create a NFT: ")
    if nft_counts.isdigit():
        count=0
        while True: 
            
           count+=1
           value = input(f"{count}.Title Enter a image a png format: ")
           if value=="exit":
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
        
 

 
