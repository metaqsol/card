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
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Screenshot import Screenshot_Clipping
from PIL import Image
import os
from Misc import getVKCode,getChromeOption,config_init,getVKCode_Hana,getVKCode_KB,getMyWebDriver
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path
import importlib
import uuid

class KookminCard:
    login_url:str =  "https://m.kbcard.com/CMN/DVIEW/MOBMCXHIAMBC0001"
    benefit_url:str = "https://m.kbcard.com/MKB/DVIEW/MMBMCXHIABNSD0006"
    driver:webdriver  = None
    mydata:list = None
    TIME_WAIT=5

    def __init__ (self,driver:webdriver,username:str,password:str):
        self.username = username
        self.password = password
        self.driver = driver

    def close_alert(self):
        wait = WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert.dismiss()
        time.sleep(2)

    def benefit(self):
        self.driver.get(self.benefit_url)
        self.mydata=list()
        ss =  Screenshot_Clipping.Screenshot()
        self.mydata.append(ss.full_Screenshot(self.driver, save_path=r'.', image_name=str(uuid.uuid4())+".png"))
        time.sleep(1)
        return self.mydata

    def clear(self):
        for file in self.mydata:
            os.remove(file)



    def login(self):
        driver = self.driver
        driver.get(self.login_url)
        try:
            self.close_alert()
        except:
            pass
        driver.find_element(By.XPATH,"//a[text()='?????????']").click()
        driver.implicitly_wait(self.TIME_WAIT)
        driver.find_element(By.ID,"userId").send_keys(self.username)
        self.driver.find_element(By.ID,"userPwd").click()
        time.sleep(4)
        for l in self.password:
            ll = getVKCode_KB(l)
            for lll in ll:
                self.driver.find_element(By.XPATH,f"//div[@aria-label='{lll}']").click()
                time.sleep(1)        
        for elem in self.driver.find_elements(By.XPATH,f"//div[@aria-label='????????????']"):
            try:
                elem.click()
                break
            except:
                continue
        self.driver.find_element(By.XPATH,f"//a[text()='?????????' and @id='btnIdPwdLogin']").click()
        time.sleep(5)

if __name__ == '__main__':
    myconf = config_init()
    myname = Path(__file__).stem
    my_module = importlib.import_module(myname)
    MyClass = getattr(my_module, myname)
    driver = getMyWebDriver("CHROME",isHeadless=False)
    driver.set_window_position(0,0)
    driver.set_window_size(820,1180)
    time.sleep(3)
    card = MyClass(driver,str(myconf[myname]["ID"]).strip(),str(myconf[myname]["PW"]).strip())
    card.login()
    print(card.benefit())
