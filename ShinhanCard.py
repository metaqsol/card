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
from Misc import getVKCode,getChromeOption,config_init,getMyWebDriver
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

class ShinhanCard:
    login_url:str =  "https://www.shinhancard.com/mob/MOBFM001N/MOBFM001C01.shc"
    benefit_url:str = "https://www.shinhancard.com/mob/MOBFM031N/MOBFM031R01.shc"
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
        self.mydata=list()
        self.close_alert()
        self.driver.get(self.benefit_url)


        summary = self.__class__.__name__+"\n"
        title=""
        total=""

        ss =  Screenshot_Clipping.Screenshot()
        self.driver.implicitly_wait(TIME_WAIT)

        elements_cnt = len(self.driver.find_elements(By.XPATH,'//*[@class="list4-item"]'))
        for i in range(elements_cnt):
            self.driver.get(self.benefit_url)
            ele = self.driver.find_elements(By.XPATH,'//*[@class="list4-item"]')[i]
            ele.click()
            time.sleep(5)

            self.driver.find_element(By.TAG_NAME,'html').send_keys(Keys.HOME)
            time.sleep(1)
            self.mydata.append(ss.full_Screenshot(self.driver, save_path=r'.', image_name=str(uuid.uuid4())+".png"))
            time.sleep(1)
            self.driver.find_element(By.TAG_NAME,'html').send_keys(Keys.HOME)
            time.sleep(1)


            title =   self.driver.find_element(By.XPATH,'//*[@id="contents"]/div/div[3]/div[1]/div/div[2]/strong').get_attribute("innerHTML")
            total = self.driver.find_element(By.XPATH,'//*[@id="cmtAmount0"]').text
            summary+=f"{title}:{total}\n"
            time.sleep(3)


            # print(element.text)
            # elements = element.find_element(By.XPATH,'/a/div[2]/div[1]')


        print("DONE")
        return self.mydata, summary  


    def benefit2(self):
        self.mydata=list()
        self.close_alert()
        self.driver.get(self.benefit_url)

        try:
            elem = self.driver.find_element(By.XPATH, '//header[@id="header"]')
            # driver.execute_script("arguments[0].setAttribute('value',arguments[1])",elem, 'none')web
            self.driver.execute_script("arguments[0].style.display = 'none';",elem)
        except Exception as e:
            logging.info(e)
            pass

        summary = self.__class__.__name__+"\n"
        title=""
        total=""






        ss =  Screenshot_Clipping.Screenshot()
        self.driver.implicitly_wait(TIME_WAIT)
        elememts = self.driver.find_elements(By.XPATH,"//span[@class='chk_icon_wrap']")
        time.sleep(2)
        for ele in elememts:
            ele.click()
            time.sleep(2)
            for e in self.driver.find_elements(By.XPATH,"//div[@class='myinfo_card_wrap']//button[@class='acc_btn toggle_btn medium']"):
                e.click()
                time.sleep(1)

            for e in self.driver.find_elements(By.XPATH,"//div[@class='myinfo_card_wrap']//dd[@class='accordion_body']"):
                self.driver.execute_script("arguments[0].style.display = 'block';",e)
                time.sleep(1)


            self.driver.find_element(By.TAG_NAME,'html').send_keys(Keys.HOME)
            time.sleep(1)
            self.mydata.append(ss.full_Screenshot(self.driver, save_path=r'.', image_name=str(uuid.uuid4())+".png"))
            time.sleep(1)
            self.driver.find_element(By.TAG_NAME,'html').send_keys(Keys.HOME)
            time.sleep(1)

            title =  self.driver.find_element(By.XPATH,'//*[@id="contents"]/div/div[3]/div[3]/div/span/button/span').get_attribute("innerHTML")
            total = self.driver.find_element(By.XPATH,'//*[@id="fm_cmt_uea0"]').text
            summary+=f"{title}:{total}\n"
            try:
                next_button:WebElement = self.driver.find_element(By.XPATH," //div[@class='card_swiper gap55_35']//button[@class='nav-button-next']")

                next_button.click()
            except:
                break
            time.sleep(3)



        return self.mydata, summary   


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
        try:
            self.driver.find_element(By.XPATH,"//label[@for='install02']").click()
            self.driver.implicitly_wait(TIME_WAIT)
        except:
            logging.info("NO ACTIVEX")
            pass

        # popup_buttons = driver.find_elements(By.XPATH,"//button[@class='btn-close-ban']")
        # #### Disable Pop Up
        # for popup in popup_buttons:         
        #     if(popup.size['width']>0):
        #         mypopup_button = popup
        time.sleep(3)
  
        self.close_alert()
        time.sleep(3)
        self.driver.find_element(By.XPATH,"//button[text() = '다른 로그인 방식 선택']").click()
        self.driver.implicitly_wait(TIME_WAIT)
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="popLogin"]/article/div[2]/ul/li[2]/button').click()
        self.driver.implicitly_wait(TIME_WAIT)
        self.driver.find_element(By.XPATH,"//input[@id='t01.memid']").send_keys(self.username)
        self.driver.find_element(By.XPATH,"//button[@id='nextBtn']").click() 
        time.sleep(3)
        self.driver.find_element(By.XPATH,'//*[@id="step02"]/div[2]/div').click()
        time.sleep(3)

        for l in self.password:
            ll = getVKCode(l)
            for kGroup,lll in ll:
                self.driver.find_element(By.XPATH,f"//div[@class='{kGroup}']/img[@class='kpd-data' and @aria-label='{lll}']").click()
                time.sleep(0.5)        
        for elem in self.driver.find_elements(By.XPATH,f"//img[@class='kpd-data' and @aria-label='확인']"):
            try:
                elem.click()
                break
            except:
                continue
        time.sleep(2)
        self.driver.find_element(By.XPATH,f"//button[@id='loginBtn']").click()




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

