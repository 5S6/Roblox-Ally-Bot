from colorama import Fore, init, Style
from sys import exit
from time import sleep
from threading import Thread
from random import randint, choice
import ctypes
from requests import get, post, delete, exceptions
from json import loads


def Logo():
   init()
   print(Fore.GREEN + r"""

   _____  .__  .__          __________        __   
  /  _  \ |  | |  | ___.__. \______   \ _____/  |_ 
 /  /_\  \|  | |  |<   |  |  |    |  _//  _ \   __\
/    |    \  |_|  |_\___  |  |    |   (  <_> )  |  
\____|__  /____/____/ ____|  |______  /\____/|__|  
        \/          \/              \/
   """)
   print(Fore.GREEN + "Made by Alek#2022")


def Options():
   print(Style.RESET_ALL)
   print("[" + Fore.GREEN + "1" + Style.RESET_ALL + "] Roblox Ally Bot")
   Option = input("Enter your choice: ")
   return int(Option)

def return_Proxies():
   try:
       proxies = open('proxies.txt','r').read().splitlines()
       if len(proxies) == 0:
           print("Error: Proxy file is empty")
           sleep(2)
           exit()
       proxies = [{'https':'http://'+proxy} for proxy in proxies]
       return proxies
   except Exception as Error:
       print(f"Error: {Error}")

csrfToken = None

def Return_Config():
   myfile = loads(open("config.json").read())
   return myfile

def UpdateCsrf(cookies):
   while True:
       try:
           global csrfToken
           csrfToken = post('https://catalog.roblox.com/v1/catalog/items/details', cookies=cookies).headers["x-csrf-token"]
           sleep(15)
       except KeyError:
           pass

AllyIds = []

def AllyBot(range1, range2, proxies, cookies, SelfGroup):
   while True:
       try:
           RandomAllyId = randint(range1, range2)
           if RandomAllyId not in AllyIds:
               AllyIds.append(RandomAllyId)    
               headers = {"X-CSRF-TOKEN": csrfToken}
               r = post(f"https://groups.roblox.com/v1/groups/{SelfGroup}/relationships/allies/{RandomAllyId}", headers=headers, cookies=cookies, proxies=choice(proxies))
               if r.json() == {}:
                   print(f"Sent an ally request to {RandomAllyId}")
       except exceptions.ProxyError as Error:
           pass
       except exceptions.ConnectionError:
           pass
   

Logo()
Option = Options()
if Option == 1:
   SelfGroup = input("Enter your groupId: ")
   cookies = {'.ROBLOSECURITY': Return_Config()['cookie']}
   Range1, Range2 = Return_Config()['Range1'], Return_Config()['Range2']
   proxies = return_Proxies()
   Thread(target=UpdateCsrf, args=[cookies]).start()
   for loop in range(4000):
       Thread(target=AllyBot, args=[Range1, Range2, proxies, cookies, SelfGroup]).start()
   
