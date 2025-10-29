import random
import string
import threading
from datetime import datetime, timedelta
import sys
import tempfile, shutil, psutil, subprocess, os, time
from pathlib import Path
import json
import re
import pyautogui as pg
import pygetwindow as gw
import ctypes
from pywinauto import Desktop
import clipboard as cb
import requests
from requests import get
import zipfile
from openpyxl import load_workbook

# from selenium.webdriver import Keys
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
# from selenium.common.exceptions import WebDriverException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# import chromedriver_autoinstaller
from ppadb.client import Client as AdbClient
# import keyboard
import tkinter as tk
from tkinter import *
from tkinter import ttk
import winsound as ws
import glob
import asyncio
import winsound as sd
import getpass
import math
import ctypes

import winsound as sd




def changeIp():
    try:
        print('아이피 변경 언제??')
        os.system('adb server start')
        client = AdbClient(host="127.0.0.1", port=5037)
        device = client.devices()  # 디바이스 1개

        if len(device) == 0:
            print('디바이스가 없냐 왜;;;')

        print(device)
        ondevice = device[0]
        print(f"온디바이스ondevice : {ondevice}")
        ondevice.shell("input keyevent KEYCODE_POWER")
        ondevice.shell("svc data disable")
        ondevice.shell("settings put global airplane_mode_on 1")
        ondevice.shell("am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true")
        time.sleep(0.5)
        ondevice.shell("svc data enable")
        ondevice.shell("settings put global airplane_mode_on 0")
        ondevice.shell("am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false")
        print('아이피 변경 함??')
        time.sleep(3)
        while True:
            
            try:
                wait_float(0.5, 0.9)
                getIp = requests.get("https://api.ip.pe.kr/json/").json()['ip']
                if getIp is not None:
                    break
            except:
                continue
    except Exception as e:
        print(e)
        while True:
            try:
                wait_float(0.5, 0.9)
                getIp = requests.get("https://api.ip.pe.kr/json/").json()['ip']
                if getIp is not None:
                    break
            except:
                continue
    return getIp




def wait_float(start, end):
    wait_ran = random.uniform(start, end)
    time.sleep(wait_ran)


def wait_float_timer(start, end, show=True):
    wait_ran = random.uniform(start, end)
    total = int(wait_ran)

    if show:
        print(f"[INFO] 대기 시작: {wait_ran:.2f}초 예정")

    for sec in range(total, 0, -1):
        if show:
            print(f"[INFO] 남은 시간: {sec}초")
        time.sleep(1)

    # 잔여 소수점(0~1초 미만)도 정확히 기다림
    remainder = wait_ran - total
    if remainder > 0:
        time.sleep(remainder)

    if show:
        print("[INFO] 대기 완료 ✅")



# driver.quit() 대신 사용! (크롬 드라이버 및 크롬 프로세스 완전 종료)
def close_driver(driver, service, user_data_dir):
    # 1) 정상 종료 시도
    print("1) 정상 종료 시도")
    try: driver.quit()
    except: pass
    time.sleep(0.3)

    # 2) chromedriver 및 자식 프로세스 강제 종료 (내가 띄운 것만)
    print("2) chromedriver 및 자식 프로세스 강제 종료 (내가 띄운 것만)")
    try:
        if service and service.process:
            p = psutil.Process(service.process.pid)
            # 자식부터 kill
            for child in p.children(recursive=True):
                try: child.kill()
                except: pass
            try: p.kill()
            except: pass
    except: pass

    # 3) 혹시 남은 Chrome 중에 "내 user-data-dir"을 쓰는 것만 골라서 kill
    print("3) 혹시 남은 Chrome 중에 '내 user-data-dir'을 쓰는 것만 골라서 kill")
    try:
        for proc in psutil.process_iter(["pid","name","cmdline"]):
            name = (proc.info["name"] or "").lower()
            cmd  = " ".join(proc.info.get("cmdline") or [])
            if "chrome" in name and user_data_dir and user_data_dir in cmd:
                try: proc.kill()
                except: pass
    except: pass

    # 4) 임시 프로필 폴더 정리
    print('4) 임시 프로필 폴더 정리')
    try: shutil.rmtree(user_data_dir, ignore_errors=True)
    except: pass