from curses.ascii import isalpha
from gc import isenabled
from turtle import isvisible
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Screenshot import Screenshot_Clipping
from PIL import Image
import os
from Misc import getVKCode,getChromeOption,config_init,getVKCode_Hana
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
import logging
import uuid
from pathlib import Path
import importlib

from typing import Optional



if __name__ == '__main__':
    myconf = config_init()
    myname = Path(__file__).stem
    my_module = importlib.import_module(myname)
    MyClass = getattr(my_module, myname)
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s,options=getChromeOption())
    driver.set_window_position(0,0)
    driver.set_window_size(820,1180)
    time.sleep(3)
    card = MyClass(driver,str(myconf[myname]["ID"]).strip(),str(myconf[myname]["PW"]).strip())
    card.login()
    print(card.benefit())

