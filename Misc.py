"""
 Copyright (c) 2022 MetaQ Solution (https://metaqsol.com)

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
 """

from curses.ascii import isalpha
from selenium import webdriver
from configparser import ConfigParser
import os
from pathlib import Path
from slack_sdk import WebClient
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def getVKCode(letter):
    ll=list()
    if letter.isalpha():
        if letter.isupper():
            ll.append('쉬프트')
            ll.append(f"대문자 {letter}")
            ll.append('쉬프트')
        else:
            ll.append(f"소문자 {letter}")
    elif letter=='@':
        ll.append('특수문자')
        ll.append('골뱅이')
        ll.append('소문자')
    elif letter=='!':
        ll.append('특수문자')
        ll.append('느낌표')
        ll.append('소문자')
    else:
        ll.append(letter)
    return ll

def getVKCode_KB(letter):
    ll=list()
    if letter.isalpha():
        if letter.isupper():
            ll.append('쉬프트')
            ll.append(f"대문자{letter}")
            ll.append('쉬프트')
        else:
            ll.append(f"{letter}")
    elif letter=='@':
        ll.append('특수키')
        ll.append('골뱅이')
        ll.append('특수키')
    else:
        ll.append(letter)
    return ll




def getVKCode_Hana(letter):
    ll=list()
    if letter.isalpha():
        if letter.isupper():
            ll.append('대문자변환')
            ll.append(f"대문자{letter}")
        else:
            ll.append(f"소문자{letter}")
    elif letter=='@':
        ll.append('특수문자변환')
        ll.append('골뱅이')
        ll.append('소문자변환')
    elif letter=='!':
        ll.append('특수문자변환')
        ll.append('느낌표')
        ll.append('소문자변환')
    else:
        ll.append(letter)
    return ll    

if __name__ == '__main__':
    getVKCode('asdf')


def getMyWebDriver(TYPE):
    driver=None
    if TYPE=="CHROME":
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s,options=getChromeOption())
        driver.set_window_position(0,0)
        driver.set_window_size(820,11180)
    elif TYPE=="EDGE":
        driver = webdriver.Edge(executable_path = os.path.join(Path(__file__).parent, "msedgedriver.exe"))
    else:
        raise Exception("Not Support")
    return driver


def getChromeOption():
    mobile_emulation = { 
        #"deviceName": "Apple iPhone 3GS"
        #"deviceName": "Apple iPhone 4"
        #"deviceName": "Apple iPhone 5"
        #"deviceName": "Apple iPhone 6"
        #"deviceName": "Apple iPhone 6 Plus"
        #"deviceName": "BlackBerry Z10"
        #"deviceName": "BlackBerry Z30"
        #"deviceName": "Google Nexus 4"
        # "deviceName": "Google Nexus 5"
        #"deviceName": "Google Nexus S"
        #"deviceName": "HTC Evo, Touch HD, Desire HD, Desire"
        #"deviceName": "HTC One X, EVO LTE"
        #"deviceName": "HTC Sensation, Evo 3D"
        #"deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black"
        #"deviceName": "LG Optimus G"
        #"deviceName": "LG Optimus LTE, Optimus 4X HD" 
        #"deviceName": "LG Optimus One"
        #"deviceName": "Motorola Defy, Droid, Droid X, Milestone"
        #"deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2"
        #"deviceName": "Motorola Droid Razr HD"
        #"deviceName": "Nokia C5, C6, C7, N97, N8, X7"
        #"deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900"
        #"deviceName": "Samsung Galaxy Note 3"
        #"deviceName": "Samsung Galaxy Note II"
        #"deviceName": "Samsung Galaxy Note"
        #"deviceName": "Samsung Galaxy S III, Galaxy Nexus"
        #"deviceName": "Samsung Galaxy S, S II, W"
        #"deviceName": "Samsung Galaxy S4"
        #"deviceName": "Sony Xperia S, Ion"
        #"deviceName": "Sony Xperia Sola, U"
        #"deviceName": "Sony Xperia Z, Z1"
        #"deviceName": "Amazon Kindle Fire HDX 7″"
        #"deviceName": "Amazon Kindle Fire HDX 8.9″"
        #"deviceName": "Amazon Kindle Fire (First Generation)"
        #"deviceName": "Apple iPad 1 / 2 / iPad Mini"
        #"deviceName": "Apple iPad 3 / 4"
        #"deviceName": "BlackBerry PlayBook"
        #"deviceName": "Google Nexus 10"
        #"deviceName": "Google Nexus 7 2"
        #"deviceName": "Google Nexus 7"
        #"deviceName": "Motorola Xoom, Xyboard"
        #"deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1"
        #"deviceName": "Samsung Galaxy Tab"
        #"deviceName": "Notebook with touch"
        "deviceName" : "iPad Air"
        
        # Or specify a specific build using the following two arguments
        #"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        #"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
	}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('window-size=820x1180')
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('headless')

    return chrome_options

def config_init():
    CONFIGFILE =  os.path.join(Path(__file__).parent, "config.ini") 
    parser = ConfigParser()
    try:
        parser.read(CONFIGFILE, encoding="utf-8")
    except:
        parser.read(CONFIGFILE)
    return parser



def send_slack(slack_token:str, myfile:str, channel:str, title:str, extension:str):
    client = WebClient(token=slack_token)
    client.files_upload(channels=channel,
                                            file=myfile,
                                            title=title,
                                            filetype=extension)
