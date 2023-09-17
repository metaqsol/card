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
from Misc import getVKCode,getChromeOption,config_init,getVKCode_Hana,getMyWebDriver
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

TIME_WAIT=5

class HanaCard:
    login_url:str =  "https://m.hanacard.co.kr/MKLGN2001M.web"
    benefit_url:str = "https://m.hanacard.co.kr/MKBENF3010M.web?CD_IDX=1&_frame=noX"
    payment_url:str = "https://m.hanacard.co.kr/MKPAMT1010M.web?_frame=noX"
    driver:webdriver  = None
    mydata:list = None

    def __init__ (self,driver:webdriver,username:str,password:str):
        self.username = username
        self.password = password
        self.driver = driver

    def close_alert(self):
        try:
            self.driver.find_element(By.XPATH,"//div[@id='admPopup']//button[@class='btn_close ui-pop-close']").click()
        except Exception as e:
            logging.info(e)
            pass

    def benefit(self):
        self.driver.get(self.benefit_url)
        summary = self.__class__.__name__+"\n"

        title = self.driver.find_element(By.XPATH,'//*[@id="frm"]/div[1]/div[1]/div[2]/button').text
        total = self.driver.find_element(By.XPATH,'//*[@id="frm"]/div[1]/div[2]/div/div[2]/dl/dd/span').text
        
        self.mydata=list()
        ss =  Screenshot_Clipping.Screenshot()
        self.mydata.append(ss.full_Screenshot(self.driver, save_path=r'.', image_name=str(uuid.uuid4())+".png"))
        time.sleep(1)

        summary+=f"{title}:{total}\n"


        summary+=f'{self.expectedPayment()}\n'
        return self.mydata,summary

    def expectedPayment(self):
        self.driver.get(self.payment_url)
        time.sleep(1)
        # try:
        #     self.driver.find_element(By.XPATH,'//*[@id="checkNoti20"]').click()
        # except:
        #     pass

        payment =  self.driver.find_element(By.XPATH,'//*[@id="frm"]/div[4]/div[2]/div/div[1]/div/div[2]')

        return f"예정금액\n{payment.text}"
    
    def clear(self):
        for file in self.mydata:
            try:
                os.remove(file)
            except:
                pass
    def login(self):
        self.driver.get(self.login_url)
        self.driver.implicitly_wait(TIME_WAIT)
        time.sleep(3)

        self.driver.find_element(By.XPATH,"//input[@id='USER_ID']").click()
        time.sleep(2)


        self.driver.find_element(By.XPATH,"//input[@id='USER_ID']").send_keys(self.username)

        self.driver.find_element(By.XPATH,"//input[@id='PASSWORD']").click()


        for l in self.password:
            ll = getVKCode_Hana(l)
            for lll in ll:
                self.driver.find_element(By.XPATH,f"//button[contains(@class,'kpdBtn') and @aria-label='{lll}']").click()
                time.sleep(0.5)        
        for elem in self.driver.find_elements(By.XPATH,f"//button[contains(@class,'kpdBtn') and @aria-label='입력완료']"):
            try:
                elem.click()
                break
            except:
                continue
        time.sleep(2)

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
    