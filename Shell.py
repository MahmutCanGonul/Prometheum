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
import git
from github import Github
import yara
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
import exifread
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone
from web3 import Web3 #web3 package version 5.5.0
from flask import Flask,jsonify
import GenerateNFT
from time import sleep
import random
 


 
"""
import scapy.all as scapy
import re

def WifiScanner():
    print("If you want exit, please enter 'exit' ")
    ip_add_range_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
    error =False
# Get the address range to ARP
    while True:
       
       ip_add_range_entered = input("\nPlease enter the ip address and range that you want to send the ARP request to (ex 192.168.1.0/24): ")
       if ip_add_range_entered == 'exit':
           break
       try: 
           if ip_add_range_pattern.search(ip_add_range_entered):
              print(f"{ip_add_range_entered} is a valid ip address range")
              break
           else:
               print(f"{ip_add_range_entered} is a invalid ip address range! Check agein ip address")
       except:
           error = True
           print(f"{ip_add_range_entered} is a invalid ip address range! Check agein ip address")
           

# Try ARPing the ip address range supplied by the user. 
# The arping() method in scapy creates a pakcet with an ARP message 
# and sends it to the broadcast mac address ff:ff:ff:ff:ff:ff.
# If a valid ip address range was supplied the program will return 
# the list of all results.
    if error == False:
        if ip_add_range_entered != 'exit':
            arp_result = scapy.arping(ip_add_range_entered)
            print(arp_result)

"""
"""
def Storj():
    username = input("Enter a Username: ")
    password = input("Enter a Password: ")
    
    if username and password:
        (private_key, public_key) = storj.generate_new_key_pair()
        storj.authenticate(email=username,password=password)
        storj.public_keys.add(public_key)
        storj.authenticate(ecdsa_private_key=private_key)
        print(private_key)
        print(public_key)
    
"""    
    


def Vpn():
    codeList = ["TR", "US-C", "US", "US-W", "CA", "CA-W",
            "FR", "DE", "NL", "NO", "RO", "CH", "GB", "HK"]
    enter_time = datetime.datatime.now()
    print("' q' --> Disconnect Vpn")
    print(" 'v' --> Change Vpn Location")
    code = random.choice(codeList)
    try:
        os.system("windscribe connect")
        while True:
            
            if 0xFF == ord("q"):
                os.system("windscribe disconnect")
                print("Disconnected the VPN!")
                exit_time = datetime.datetime.now() - enter_time
                print(f"Passed Time {exit_time}")
                break
            elif 0xFF == ord("v"):
                code = random.choice(codeList)
                print("Changing the IP Address.....")
            
            
            os.system("windscribe connect "+code)
                
            
            
            
    except Exception as ex:
        os.system("windscribe disconnect")
        print("Disconnected the VPN!")
        print(f"Error --> {ex}")
        


def Ethereum():
    infuro_url = "https://mainnet.infura.io/v3/f3092718f2f146169c2b1f7d53b99b7a"
    try:
        web3 = Web3(Web3.HTTPProvider(infuro_url))
        if web3.isConnected():
            print("Connect Ethereum --> True")
            print("1.Info about Ethereum")
            print("2.Send Ethereum Another Account")
             
            choice = input("Enter 1 or 2: ")
            if choice == "1":
                blocks_num = web3.eth.blockNumber
                last_block = web3.eth.getBlock('latest')
                last_block_trans = web3.eth.getBlockTransactionCount('latest')
                difficulty_last_block = last_block.difficulty
                all_trans = web3.eth.getTransactionCount
                print(f"Ethereum Block Numbers --> {blocks_num}")
                print(f"Ethereum All Transactions Number --> {all_trans}") 
                print(f"Ethereum Last Block Transactions Number --> {last_block_trans}") 
                print(f"Ethereum Difficulty --> {difficulty_last_block}")
                print(web3.toJSON(last_block))
            elif choice == "2":
                ganache_url = "https://mainnet.infura.io/v3/f3092718f2f146169c2b1f7d53b99b7a"
                web3 = Web3(Web3.HTTPProvider(ganache_url))
                account_1 = input("Enter a Your Ethereum Address: ")
                if account_1:
                    balance = web3.eth.getBalance(account_1)
                    print(f"ETH Balance In Your Address: {balance}")
                    account_2 = input("Enter a Another Ethereum Address: ")
                    if account_2:
                        balance2= web3.eth.getBalance(account_2)
                        print(f"ETH Balance In Another Address: {balance2}")
                        private_key = input("Enter a Your Private Key: ")
                        value =   input("Enter a ETH Amount: ")
                        nonce = web3.eth.getTransactionCount(account_1)
                        if private_key and value:
                               tx = {'nonce':nonce,
                                  'to':account_2,
                                  'value':web3.toWei(float(value),'ether'),
                                  'gas':200000,
                                  'gasPrice':web3.toWei('50','gwei')}
                               signed_tx = web3.eth.account.signTransaction(tx,private_key)
                               tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
                               print(f"Transaction is success! Hash --> {tx_hash}")
                        else:
                            print("Transaction --> Error")
        else:
            print("Connect Ethereum --> False")
    except:
          print("Ethereum Situation --> Error")        
    
    


def ListFiles(path):
    arr = os.listdir(path)
    if len(arr) > 0:
        for i in range(len(arr)):
            print(arr[i])

def PhoneNumberInfo():
    phoneNumber = input("Enter a phone number: ")
    if '+' in phoneNumber:
        try:
            ch_number = phonenumbers.parse(phoneNumber,"CH")
            country = geocoder.description_for_number(ch_number,"en")
            ro_number = phonenumbers.parse(phoneNumber,"RO")
            operator = carrier.name_for_number(ro_number,"en")
            gb_number = phonenumbers.parse(phoneNumber, "GB")
            timeZone = timezone.time_zones_for_number(gb_number)
            print(f"Country --> {country} && Operator --> {operator}")
            print(f"Location --> {timeZone}")
             
        except:
            print("Invalid phone number!")
    else:
        print("Add '+' for the phone number!")
            
            

def create_google_maps_url(gps_coords): 
    print(gps_coords["lat"][0])  
    print(gps_coords["lat"][1])   
    print(gps_coords["lat"][2])
    print(gps_coords["lat_ref"])
    
    print(gps_coords["lon"][0])  
    print(gps_coords["lon"][1])   
    print(gps_coords["lon"][2])
    print(gps_coords["lon_ref"])
    
    lat_1 = str(gps_coords["lat"][0])
    lat_1 = lat_1.replace('(','')
    lat_1 = lat_1.replace(')','')
    
    lat_2 = str(gps_coords["lat"][1])
    lat_2 = lat_2.replace('(','')
    lat_2 = lat_2.replace(')','')
    
    lat_3 = str(gps_coords["lat"][2])
    lat_3 = lat_3.replace('(','')
    lat_3 = lat_3.replace(')','')
    
    lon_1 = str(gps_coords["lon"][0])
    lon_1 = lon_1.replace('(','')
    lon_1 = lon_1.replace(')','')
    
    lon_2 = str(gps_coords["lon"][1])
    lon_2 = lon_2.replace('(','')
    lon_2 = lon_2.replace(')','')
    
    lon_3 = str(gps_coords["lon"][2])
    lon_3 = lon_3.replace('(','')
    lon_3 = lon_3.replace(')','')
    
    result = lat_1.split(',')
    result2 = lat_2.split(',')
    result3 = lat_3.split(',')
    result4 = lon_1.split(',')
    result5 = lon_2.split(',')
    result6 = lon_3.split(',')
    
    degress =[]
    degress.append(float(float(result[0])) / float(result[1]))
    degress.append(float(float(result2[0])) / float(result2[1]))
    degress.append(float(float(result3[0])) / float(result3[1]))
    degress.append(float(float(result4[0])) / float(result4[1]))
    degress.append(float(float(result5[0])) / float(result5[1]))
    degress.append(float(float(result6[0])) / float(result6[1]))
    # Exif data stores coordinates in degree/minutes/seconds format. To convert to decimal degrees.
    # We extract the data from the dictionary we sent to this function for latitudinal data.
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
    # We extract the data from the dictionary we sent to this function for longitudinal data.
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    # We return a search string which can be used in Google Maps
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


def CreateGoogleURLOption2(path):
    if '.jpg' or '.jpeg' or '.png' or '.jfif' in path:
        try:
            tags = exifread.process_file(open(path,'rb'))
            geo = {i:tags[i] for i in tags.keys() if i.startswith('GPS')}
            print(geo)
            if geo:
                gps_lat = geo['GPS GPSLatitude']
                gps_lon = geo['GPS GPSLongitude']
                gps_date = geo['GPS GPSDate']
                print(f"Date ---> {gps_date}")
                print(f"https://maps.google.com/?q={gps_lat},{gps_lon}")
            else:
                print("There is no GPS Info!")
                
        except:
            print("There is no GPS Info!")
    else:
        if path:
            print("Invalid path!")
    

# Converting to decimal degrees for latitude and longitude is from degree/minutes/seconds format is the same for latitude and longitude. So we use DRY principles, and create a seperate function.
def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    # A value of "S" for South or West will be multiplied by -1
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees

def FindLocationFromImage():
     
     
    file = input("Enter a from local image path: ")
    CreateGoogleURLOption2(file)
    if len(file) > 0:
        control = file.split('.')
        if control[len(control)-1] == "jpg" or control[len(control)-1] == "jpeg" or control[len(control)-1] == "png" or control[len(control)-1] == "jfif":
             
            try:
               image = Image.open(file)
               print(f"_______________________________________________________________{file}_______________________________________________________________")
               gps_coords = {}
               # We check if exif data are defined for the image. 
               if image._getexif() == None:
                  print(f"{file} contains no exif data.")
               else:    
                   for tag, value in image._getexif().items():
                # If you print the tag without running it through the TAGS.get() method you'll get numerical values for every tag. We want the tags in human-readable form. 
                # You can see the tags and the associated decimal number in the exif standard here: https://exiv2.org/tags.html
                       tag_name = TAGS.get(tag)
                       print(tag_name)
                       if tag_name == "GPSInfo":
                          for key, val in value.items():
                        # Print the GPS Data value for every key to the screen.
                             print(f"{GPSTAGS.get(key)} - {val}")
                        # We add Latitude data to the gps_coord dictionary which we initialized in line 110.
                             if GPSTAGS.get(key) == "GPSLatitude":
                                gps_coords["lat"] = val
                        # We add Longitude data to the gps_coord dictionary which we initialized in line 110.
                             elif GPSTAGS.get(key) == "GPSLongitude":
                                gps_coords["lon"] = val
                        # We add Latitude reference data to the gps_coord dictionary which we initialized in line 110.
                             elif GPSTAGS.get(key) == "GPSLatitudeRef":
                                gps_coords["lat_ref"] = val
                        # We add Longitude reference data to the gps_coord dictionary which we initialized in line 110.
                             elif GPSTAGS.get(key) == "GPSLongitudeRef":
                                gps_coords["lon_ref"] = val 
                       else:
                          print(f"{tag_name} - {value}")
                   if gps_coords:
                      print(create_google_maps_url(gps_coords))  
                   else:
                      print()
            except:
               print("File format not supported or can not find a location!")
     

def SpeedTest():
    try:
        test = speedtest.Speedtest()
        print("Performing download test...")
        download_perform = test.download()
        print("Performing upload test...")
        upload_perform = test.upload()
        ping_perform = test.results.ping
    
        print(f"Download speed: {download_perform /1024 / 1024:.2f} Mbit/s")
        print(f"Upload speed: {upload_perform /1024 / 1024:.2f} Mbit/s")
        print(f"Ping: {ping_perform:.2f} ms")
    except:
        print("Something get error try later...")
    
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

def github(path):
    access_tok = input("Enter a Own Access Token in Github: ")
    if access_tok:
        try:
            g = Github(access_tok)
            while True:
                print("'clone' --> Clone the repo on your directory")
                print('repo.name --> See the all repo names')
                print("'search_language' --> Show the repo from the language")
                print("'repo.files' --> Show the files in repo")
                print("'repo.traffic' --> Show the repo clone and view traffic")
                print("'repo.branches' --> Show the branches in repo")
                print("'exit' --> exit the platfrom")
                choice = input("Enter a Choice: ")
                if choice == "clone":
                    repo_url = input("Enter the target repo url: ")
                    if repo_url:
                       your_file = path
                       if your_file:
                          print("Process...")
                          git.Git(your_file).clone(repo_url)
                          print("Success! Repo clone on ",your_file)
                elif choice == "repo.name":
                    for repo in g.get_user().get_repos():
                        name = repo.name
                        stars= repo.stargazers_count
                        print(f"-->Name:{name} Star:{stars}")
                elif choice == "exit":
                    break
                elif choice == "search_language":
                    soft = input("Enter a software language: --> 'python','c','c#','ruby' ")
                    if soft:
                         repos = g.search_repositories(query=f'language:{soft}')
                         for repo in repos:
                             print(repo)
                elif choice == "repo.files":
                    repo_name = input("Enter a repo name: ")
                    if repo_name:
                        repo = g.get_user().get_repo(repo_name)
                        print(repo)
                        contents = repo.get_contents("")
                        for file in contents:
                            print(file)
                elif choice == "repo.traffic":
                    repo_name = input("Enter a repo name: ")
                    if repo_name:
                       repo = g.get_user().get_repo(repo_name) 
                       contents_view = repo.get_views_traffic(per="week")
                       contents_clone = repo.get_clones_traffic(per="week")
                       print("//////////// View Traffic ////////////")
                       print(contents_view)
                       print("//////////// Clone Traffic ////////////")
                       print(contents_clone)
                elif choice == "repo.branches":
                    repo_name = input("Enter a repo name: ")
                    if repo_name:
                        repo = g.get_user().get_repo(repo_name) 
                        list(repo.get_branches())
                        
                    
                       
                       
        except Exception as ex:
            print(f"Github Error --> {ex}")
    else:
         print("You should enter a Access Token for Github Connection!")         
def History(commits):
    if len(commits) > 0:
        for i in range(len(commits)):
            print(commits[i])
    else:
        print("No commits!")
 
def MalwareDetect():
    rules_path = "C:\Malware Detect"
    #Read files
    peid_rules = yara.compile(rules_path + '\peid.yar')
    packer_rules = yara.compile(rules_path + '\packer.yar')
    crypto_rules = yara.compile(rules_path + '\crypto_signatures.yar')
    exe_file_path = input("Enter the target local file path: ")
    is_foundMalware = False
    if exe_file_path:
        try:
           matches = crypto_rules.match(exe_file_path)
           if matches:
              is_foundMalware=True 
              print('Cryptors ====> Found')
              print(matches)
        except:
        #I always add this exception thing, because I don't know what could happen
              print('cryptor exception, something get issue...')
              is_foundMalware=True
        if is_foundMalware == False:
            print("Cryptors ====> Not Found")
        
        is_foundMalware=False
        #detect packers

        try:
            matches = packer_rules.match(exe_file_path)
            if matches:
               is_foundMalware=True
               print('Packers  ====> Found')
               print(matches)
        except:
            is_foundMalware=True
            print('packer exception, something get issue...')
     
        
    if is_foundMalware == False:
        print("Packers  ====> Not Found")
        
    is_foundMalware = False
    
        
    packers = ['AHTeam', 'Armadillo', 'Stelth', 'yodas', 'ASProtect', 'ACProtect', 'PEnguinCrypt', 
 'UPX', 'Safeguard', 'VMProtect', 'Vprotect', 'WinLicense', 'Themida', 'WinZip', 'WWPACK',
 'Y0da', 'Pepack', 'Upack', 'TSULoader'
 'SVKP', 'Simple', 'StarForce', 'SeauSFX', 'RPCrypt', 'Ramnit', 
 'RLPack', 'ProCrypt', 'Petite', 'PEShield', 'Perplex',
 'PELock', 'PECompact', 'PEBundle', 'RLPack', 'NsPack', 'Neolite', 
 'Mpress', 'MEW', 'MaskPE', 'ImpRec', 'kkrunchy', 'Gentee', 'FSG', 'Epack', 
 'DAStub', 'Crunch', 'CCG', 'Boomerang', 'ASPAck', 'Obsidium','Ciphator',
 'Phoenix', 'Thoreador', 'QinYingShieldLicense', 'Stones', 'CrypKey', 'VPacker',
 'Turbo', 'codeCrypter', 'Trap', 'beria', 'YZPack', 'crypt', 'crypt', 'pack',
 'protect', 'tect'
]
    try:
       matches = peid_rules.match(exe_file_path)
       if matches:
          for match in matches:
             for packer in packers:
        #this line is simply trying to see if one of the known packers has been detected
                if packer.lower() in match.lower():
                   is_foundMalware = True
                   print('Packers  ====> Found')
                   print(packer)
    except:
          is_foundMalware=True
          print('error')
    
    if is_foundMalware == False:
        print('Packers  ====> Not Found')
 

 
commits = []
path = "{0}".format(os.getcwd())
is_cd=False
while True:
    is_cd=False
    text = input(f"prometheum: {path} ==> ")
    control_cd = text.split(None,1)
    if len(control_cd) == 2:
        if control_cd[0] == "cd":
            is_cd = True
            try:
                os.chdir(control_cd[1])
                path = "{0}".format(os.getcwd())
            except:
                print("Invalid path!")
     
                
        
    if text == "exit":
        break
    elif text == "status":
        ListFiles(path)
    elif text == "time":
        print(datetime.datetime.now())
    elif text == "time.year":
        time_now = datetime.datetime.now()
        print(time_now.year)
    elif text == "time.day":
        time_now = datetime.datetime.now()
        print(time_now.day)
    elif text == "HandRecognition.pro":
        print("If you want exit, please enter the screen and  enter the 'q' ")
        HandRecognition.main()
    elif text == "system":
         print(platform.platform())      
    elif text == "system.info":
        print(platform.uname())
    elif text == "clear":
        os.system('cls')
    elif text == "Calendar.pro":
         Calendar()
    elif text == "Ethereum.pro":
        Ethereum()
    elif  text == "NetSpeed.pro":
          SpeedTest()
    elif text == "Wikipedia.pro":
        Wikipedia()
    elif text == "Github.pro":
        github(path)
    elif text == "History.pro":
        History(commits)
    elif text == "ImageInfo.pro":
        FindLocationFromImage()
    elif text == "MalwareDetect.pro":
        MalwareDetect()
    elif text == "PhoneNumberInfo.pro":
        PhoneNumberInfo()
    elif text == "GenerateNFT.pro":
        GenerateNFT.GenerateNFT()
    elif text == "color.green":
        os.system('COLOR A')
    elif text == "color.blue":
        os.system('COLOR 9')
    elif text == "color.aqua":
        os.system('COLOR B')
    elif text == "color.red":
        os.system('COLOR C')
    elif text == "color.purple":
        os.system('COLOR D')
    elif text == "color.yellow":
        os.system('COLOR E')
    elif text == "color.white":
        os.system('COLOR F')
    else:
        
        txt = text.lower()
        if txt == "handrecognition" or txt == "hand recognition" or  txt == "handrecognition.pr" or txt == "hand recognition.pro" or txt == "handrecognition." :
            print("True syntax is ----> HandRecognition.pro")
        elif txt == "calendar" or txt == "calendar.":
            print("True syntax is ----> Calendar.pro")
        elif txt == "netspeed" or txt == "net speed" or  txt == "netspeed.pr" or txt == "net speed.pro" or txt == "netspeed." :
            print("True syntax is ----> NetSpeed.pro")
        elif txt == "wikipedia" or txt == "wikipedia.":
            print("True syntax is ----> Wikipedia.pro")
        elif txt == "github" or txt == "github.":
            print("True syntax is ----> Github.pro")
        elif txt == "color":
            print("True syntax is ---->  color.COLOR_NAME / EX: color.green")
        elif txt == "history" or  txt == "history.":
            print("True syntax is ---->  History.pro")
        elif txt == "imageinfo" or txt == "image info" or  txt == "image" or txt == "image info.pro" or txt == "imageinfo." :
            print("True syntax is ---->  ImageInfo.pro")
        elif txt == "malwaredetection" or txt == "malware detection" or  txt == "malwaredetection." or txt == "malware detection.":
            print("True syntax is ---->  MalwareDetection.pro")
        elif txt == "phone" or txt == "phonenumber" or  txt == "phonenumberinfo." or txt == "phone number." or txt == "phonenumber.":
            print("True syntax is ---->  PhoneNumberInfo.pro")
        elif txt == "ethereum" or txt == "ethereum.":
            print("True syntax is ---->  Ethereum.pro")
        elif txt == "generate" or txt == "generatenft" or txt == "nft" or txt == "generatenft.":
            print("True syntax is ---->  GenerateNFT.pro")
        else:
            if len(text)>0 and is_cd == False:
                result,error = Prometheum.run('<stdio>',text)
                if error:
                   print(error.error_message())
                elif result:
                   print(result)
    if len(text)>0:
        commits.append(text)
    
 
 
   
 
   
    
     
