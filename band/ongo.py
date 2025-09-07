import random
import string
import threading
import time
from datetime import datetime, timedelta
import sys
import os
import pyperclip
from pathlib import Path
import json
import re
import pyautogui as pg
import pygetwindow as gw
import ctypes
from pywinauto import Desktop
import clipboard as cb
import zipfile
from openpyxl import load_workbook
from selenium import webdriver
# from selenium.webdriver import Keys
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
# from selenium.common.exceptions import WebDriverException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# import chromedriver_autoinstaller
# import keyboard
import tkinter as tk
from tkinter import *
from tkinter import ttk
import winsound as ws
import glob
import asyncio
import winsound as sd
import shutil
import getpass
import math
import ctypes

import winsound as sd
import urllib.parse


def wait_float(start, end):
    wait_ran = random.uniform(start, end)
    time.sleep(wait_ran)








def bandScript(getDict):

    options = Options()
    # user_data = f'C:\\Users\\{pcUser}\\AppData\\Local\\Google\\Chrome\\User Data\\default'
    # options.add_argument(f"user-data-dir={user_data}")
    # options.add_argument(f'--profile-directory=Profile {profileInfo['pl_number']}')

    # 캐시 및 저장된 데이터 관련
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-features=TranslateUI")

    # 쿠키 및 세션 완전 초기화
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.naver.com')
    driver.set_page_load_timeout(12)
    driver.set_window_size(1300, 800)
    driver.set_window_position(0,0)
    driver.get('https://band.us')


    while True:
        wait_float(1.5, 2.5)
        try:
            loginBtn = driver.find_element(by=By.CSS_SELECTOR, value="._loginBtn")
            loginBtn.click()
            break
        except:
            pass


    while True:
        wait_float(1.5, 2.5)
        try:
            naverLoginBtn = driver.find_element(by=By.CSS_SELECTOR, value=".-naver.externalLogin")
            naverLoginBtn.click()
            break
        except:
            pass



    while True:
        wait_float(1.5, 2.5)
        try:
            idInput = driver.find_element(by=By.CSS_SELECTOR, value="#id")

            cb.copy('dhkdgkstjq11')
            wait_float(0.5,1.2)
            idInput.click()
            wait_float(0.5,1.2)
            pg.hotkey('ctrl', 'v')
            wait_float(0.5, 1.2)
        except:
            continue

        try:
            pwdInput = driver.find_element(by=By.CSS_SELECTOR, value="#pw")

            cb.copy('1e2r3tdjh3e1')
            wait_float(0.5,1.2)
            pwdInput.click()
            wait_float(0.5,1.2)
            pg.hotkey('ctrl', 'v')
            wait_float(0.5, 1.2)
        except:
            pass

        try:
            loginSuccessBtnActiveChk = driver.find_elements(by=By.CSS_SELECTOR, value=".btn_login.next_step.nlog-click.off")
            if len(loginSuccessBtnActiveChk) == 0:
                loginSuccessBtnActive = driver.find_element(by=By.CSS_SELECTOR, value=".btn_login.next_step.nlog-click")
                loginSuccessBtnActive.click()
                break

        except:
            pass


    try:
        wait_float(0.5,1.2)
        captcha = driver.find_element(by=By.CSS_SELECTOR, value=".captcha")
        if captcha:
            pg.alert('캡챠 체크!!')
    except:
        pass


    driver.get('https://www.band.us/band/57798843')


    while True:
        wait_float(1.5, 2.5)
        try:
            writeBtn = driver.find_element(by=By.CSS_SELECTOR, value="._btnPostWrite")
            writeBtn.click()
            break
        except:
            pass

    while True:
        wait_float(1.5, 2.5)
        try:
            imgUploadBtn = driver.find_element(by=By.CSS_SELECTOR, value="._btnAttachPhoto")
            imgUploadBtn.click()
        except:
            pass

        cb.copy(r'C:\Users\chang\OneDrive\바탕 화면\project\py-auto-use\band\testimg')
        wait_float(0.5,1.2)
        pg.hotkey('ctrl', 'v')
        wait_float(0.5, 1.2)
        pg.press('enter')

        wait_float(1.2, 1.5)
        cb.copy('001')
        wait_float(0.5,1.2)
        pg.hotkey('ctrl', 'v')
        wait_float(0.5, 1.2)
        pg.press('enter')

        try:
            imgUploadSuccessBtn = driver.find_element(by=By.CSS_SELECTOR, value="._submitBtn")
            imgUploadSuccessBtn.click()
            break
        except:
            pass

    blogWb = load_workbook('./etc/blog_work.xlsx')
    blogEx = blogWb.active



    

    pg.alert('잠깐만?')