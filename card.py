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

# -*- encoding:utf8 -*-
from curses.ascii import isdigit
from select import select
from turtle import Screen, isvisible
from configparser import ConfigParser
from bs4 import BeautifulSoup
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import logging
from inspect import currentframe, getframeinfo
from urllib.request import Request, urlopen
from datetime import datetime
from requests.auth import HTTPBasicAuth
from datetime import date

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from Misc import *
import importlib

import LotteCard
import ShinhanCard
import HanaCard

######################
logging.basicConfig(level=logging.INFO)


driver = getMyWebDriver("CHROME")


time.sleep(3)

######################################
myconf = config_init()

my_text = ""
for myname in myconf:
    if(myname.endswith("Card")):
        my_module = importlib.import_module(myname)
        MyClass = getattr(my_module, myname)
        try:
            card = MyClass(driver,str(myconf[myname]["ID"]).strip(),str(myconf[myname]["PW"]).strip())
            card.login()
            mydata, my_summary = card.benefit()
            my_text+=my_summary+'\n'
            for mybenefit in mydata:
                for mymsg in myconf:
                    if(mymsg.endswith('Msg')):
                        if(mymsg.startswith('Slack')):                    
                            send_slack_file(slack_token=str(myconf['Slack_Msg']['TOKEN']).strip()
                            , myfile = mybenefit
                            , channel = myconf['Slack_Msg']['CHANNEL']
                            , title=myname
                            ,extension='png')
            card.clear()

        except:
            pass


for mymsg in myconf:
    if(mymsg.endswith('Msg')):
        print("Text")
        print(my_text)
        # try:
        #     if(mymsg.startswith('Slack')):   
        #         send_slack_text(slack_token=str(myconf['Slack_Msg']['TOKEN']).strip()
        #         , channel = myconf['Slack_Msg']['CHANNEL']
        #         , text=my_text)
        # except Exception as e:
        #     print(e)
        
        try:
            if(mymsg.startswith('Kakao')):
                send_kakao(myconf['Kakao_Msg']['KEY'].strip(),my_text)
        except Exception as e:
            print(e)