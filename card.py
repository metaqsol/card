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
from selenium import webdriver
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
from Misc import getVKCode,getChromeOption,config_init,send_slack,getMyWebDriver
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

for myname in myconf:
    if(myname.endswith("Card")):
        my_module = importlib.import_module(myname)
        MyClass = getattr(my_module, myname)
        card = MyClass(driver,str(myconf[myname]["ID"]).strip(),str(myconf[myname]["PW"]).strip())
        card.login()
        for mybenefit in card.benefit():
            send_slack(slack_token=str(myconf['Slack']['TOKEN']).strip()
            , myfile = mybenefit
            , channel = myconf['Slack']['CHANNEL']
            , title=myname
            ,extension='png')
        card.clear()

