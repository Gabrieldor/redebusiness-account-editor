from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import traceback

import pandas as pd
import requests
import os
import sys
import time


class Changer():
        
    def start(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 60)

    def login(self, lg, ps):
        self.driver.get("https://www.redebusiness.com.br/")
        self.driver.find_element(By.XPATH, "//input[@id='username']").send_keys(lg)
        self.driver.find_element(By.XPATH, "//input[@id='password']").send_keys(ps)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()


    def change_date(self, date):
        day = str(int(date[-2:]))
        month = str(int(date[5:-3])-1)
        year = int(date[:4])
        self.driver.find_element(By.XPATH, "//input[@id='usr_birthday']").click()
        
        Select(self.driver.find_element(By.XPATH, "//select[@class='flatpickr-monthDropdown-months']")).select_by_value(month)
        yf = self.driver.find_element(By.XPATH, "//input[@class='numInput cur-year']")
        yf.clear()
        yf.send_keys(year)

        for elem in self.driver.find_elements(By.XPATH, "//span[@class='flatpickr-day']"):
            if elem.get_attribute("innerHTML") == day:
                elem.click()
                break


    def change_geral(self, info):
        self.driver.get("https://www.redebusiness.com.br/setting/general-setting")
        uf = self.driver.find_element(By.XPATH, "//input[@id='username']")
        uf.clear()
        uf.send_keys(info[0])

        pf = self.driver.find_element(By.XPATH, "//input[@id='phone_number']")
        pf.clear()
        pf.send_keys(info[1])

        ef = self.driver.find_element(By.XPATH, "//input[@id='email']")
        ef.clear()
        ef.send_keys(info[2])

        self.change_date(info[3])
        Select(self.driver.find_element(By.XPATH, "//select[@name='country']")).select_by_visible_text(info[4])
        Select(self.driver.find_element(By.XPATH, "//select[@name='gender']")).select_by_visible_text(info[5])
        Select(self.driver.find_element(By.XPATH, "//select[@id='weather_unit']")).select_by_visible_text(info[6].upper())
        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, "//button[@id='update_user_data']"))
        self.driver.find_element(By.XPATH, "//button[@id='update_user_data']").click()

    def change_prof(self, info):
        self.driver.get("https://www.redebusiness.com.br/setting/profile-setting")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='avatar-holder profile']")))

        sel_info = [info[9], info[14]]
        

        af = self.driver.find_element(By.XPATH, "//textarea[@id='about']")
        af.clear()
        af.send_keys(info[2])

        apf = self.driver.find_element(By.XPATH, "//textarea[@id='fid_12']")
        apf.clear()
        apf.send_keys(info[10])

        aps = self.driver.find_element(By.XPATH, "//textarea[@id='fid_13']")
        aps.clear()

        aps.send_keys(info[11])

        del info[2]
        del info[4]
        del info[7]
        del info[7]
        del info[7]
        del info[9]

        i = 0
        for elem in self.driver.find_elements(By.XPATH, "//form[@method='post']//input"):
            self.driver.execute_script("arguments[0].scrollIntoView();", elem)
            try:
                elem.clear()
            except Exception as e:
                continue
            elem.send_keys(info[i])
            i += 1
            
        Select(self.driver.find_element(By.XPATH, "//select[@id='relationship']")).select_by_visible_text(sel_info[0])
        try:
            Select(self.driver.find_element(By.XPATH, "//select[@name='fid_17']")).select_by_visible_text(sel_info[1])
        except:
            Select(self.driver.find_element(By.XPATH, "//select[@name='fid_17']")).select_by_value("9")

        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, "//button[@class='btn btn-main btn-mat btn-mat-raised add_wow_loader']"))
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-main btn-mat btn-mat-raised add_wow_loader']").click()

    def change_avatar(self, info):
        self.driver.get("https://www.redebusiness.com.br/setting/avatar-setting")
        with open("icon.png", 'wb') as f:
            f.write(requests.get(info).content)
        self.driver.find_element(By.XPATH, "//input[@id='avatar']").send_keys(os.path.dirname(os.path.abspath(sys.argv[0])) + "\icon.png")

        self.driver.execute_script("arguments[0].scrollIntoView();", self.driver.find_element(By.XPATH, "//button[@class='btn btn-main btn-mat btn-mat-raised add_wow_loader']"))
        self.driver.find_element(By.XPATH, "//button[@class='btn btn-main btn-mat btn-mat-raised add_wow_loader']").click()

    def add_endereco(self, info):
        self.driver.get("https://www.redebusiness.com.br/setting/addresses")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='address_book_innr']")))
        self.driver.find_element(By.XPATH, "//div[@class='address_book_innr']").click()
        i = 0
        time.sleep(3)
        for elem in self.driver.find_elements(By.XPATH, "//form[@class='form form-horizontal address_form']//input"):
            elem.clear()
            elem.send_keys(info[i])
            i+=1

        ef = self.driver.find_element(By.XPATH, "//textarea[@id='address']")
        ef.clear()
        ef.send_keys(info[-1])
        
        self.driver.find_element(By.XPATH, "//form[@class='form form-horizontal address_form']//button[@class='btn btn-main btn-mat']").click()

    def change(self, row):
        self.driver.maximize_window()
        try:
            try:
                self.login(row[0], row[1])
            except:
                pass
            self.change_geral(row[2:9])
            self.change_prof(row[9:29])
            self.change_avatar(row[36])
            self.add_endereco(row[37:])
            self.driver.quit()
        except:
            print(traceback.format_exc())
            self.change(row)

try:
    c = Changer()

    rows = pd.read_excel("perfis.xlsx")
    rows = rows.where(pd.notnull(rows), "")
    rows = rows.values.tolist()
    for r in rows:
        c.start()
        c.change(r)
except:
    print(traceback.format_exc())
    print("UM ERRO OCORREU PRESSIONE UMA TECLA PARA SAIR")
    input()
        