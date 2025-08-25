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
import requests
from requests import get
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
import shutil
import getpass
import math
import ctypes

import winsound as sd
from bs4 import BeautifulSoup
import urllib.parse


def create_ready_array():
    # 랜덤으로 3 또는 4를 선택합니다.
    num = random.choice([3, 4])
    # 'test' 값이 num_tests 개수만큼 들어가는 배열을 생성합니다.
    ready_array = ['notWork'] * num
    return ready_array


def create_active_array(lengthArr, innerArr, num_realworks=1):
    length = random.randint(lengthArr[0], lengthArr[1])
    array = ['notWork'] * length
    array[0] = 'notWork'
    array[-1] = 'notWork'
    
    available_positions = list(range(1, length - 1))
    
    # 뽑을 수 있는 개수보다 크게 안 뽑게 보정
    num_of_works = min(random.randint(innerArr[0], innerArr[1]), len(available_positions))
    
    work_positions = random.sample(available_positions, num_of_works)
    for pos in work_positions:
        array[pos] = 'work'
    
    if work_positions:
        num_realworks = min(num_realworks, len(work_positions))
        realwork_positions = random.sample(work_positions, num_realworks)
        for pos in realwork_positions:
            array[pos] = 'realwork'
    
    return array


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


def focus_window(winName):
    while True:
        try:
            user32 = ctypes.windll.user32
            foreground_window = user32.GetForegroundWindow()
            window = gw.Window(foreground_window)
            print(window.title)
            if winName in window.title:
                break
            else:
                windows = Desktop(backend="uia").windows()
                for window in windows:
                    if winName in window.window_text():
                        window.set_focus()
                        break
        except Exception as e:
            print(str(e))
            pass

def wait_float(start, end):
    wait_ran = random.uniform(start, end)
    time.sleep(wait_ran)

def process_array(data, dataStr, type = "free"):

    # 1. 배열을 랜덤하게 섞기
    random.shuffle(data)
    
    # 2. cw_work_count 값에 따라 정렬하기 (작은 순서)
    sorted_data = sorted(data, key=lambda x: x[dataStr])

    if len(sorted_data) == 0:
        return False
    if type == "free":
        maxNum = len(sorted_data)
        ranNum = 0
        if maxNum > 15:
            ranNum = random.randrange(13,16)
        else:
            result = math.ceil(maxNum / 2)
            ranNum = random.randrange(result,maxNum)
        # 3. 상위 15개 항목 추출
        topValue = sorted_data[:ranNum]
    else:
        topValue = sorted_data[0]

    return topValue

def active_chrome(driver):
    chrome_windows = pg.getWindowsWithTitle("Chrome")[0]
    try:
        if chrome_windows.isActive == False:
            chrome_windows.activate()
        chrome_windows.restore()
        # if chrome_windows.isMaximized == False:
        #     chrome_windows.maximize()
    except Exception as e:
        pass
        # chrome_windows.minimize()
        # chrome_windows.maximize()
    return

def check_file_exists(directory, filename):
    
    # Construct the full file path
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists
    if os.path.isfile(file_path):
        return True
    else:
        return False
    
def searchCafeContent(driver, workInfo, test = None):

    targetWorkStatus = False

    try:
        print('여기서는 카페 작업!!!')
        scrollRanVal = random.randrange(5, 12)
        errCount = 0
        while True:
            errCount += 1
            wait_float(1.2,1.9)

            try:
                topBtns = driver.find_elements(by=By.CSS_SELECTOR, value=".flick_bx")
                for topBtn in topBtns:
                    if "카페" in topBtn.text:
                        topBtn.click()
                        targetWorkStatus = True
                        break
            except:
                pass


            try:
                moreCafeBtns = driver.find_elements(by=By.CSS_SELECTOR, value=".mod_more_wrap a")
                for moreCafeBtn in moreCafeBtns:
                    if "카페" in moreCafeBtn.text:
                        moreCafeBtn.click()
                        break
            except Exception as e:
                print(str(e))
                print('카페 더보기 클릭 에러!!')
                pass

            try:
                cafeListChk = driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[1]')
                if "관련도" in cafeListChk.text:
                    break
            except Exception as e:
                print(str(e))
                print('카페 더보기 클릭 후 관련도 못찾는 에러!!')
                if errCount > 4:
                    break
                pass
        
        for i in range(2):
            pg.press('end')
            wait_float(2.1,2.9)
        

        while True:
            try:
                titleList = driver.find_elements(by=By.CSS_SELECTOR, value=".title_link")
                if len(titleList) > 0:
                    break
            except Exception as e:
                print(str(e))
                print('카페 글 리스트 못찾는 에러!!')
                pass

        # 본격적으로 게시물 찾기 없을때를 대비해 noSearchCount / noSearchStatus 준비
        noSearchCount = 0
        noSearchStatus = False

        oddCount = 0
        while True:
            oddCount += 1
            noSearchCount += 1
            if noSearchCount > 5:
                noSearchStatus = True
                return 'noSearch'
            searchSuccess = False
            try:
                for title in titleList:
                    print(f"찾을 링크 : {workInfo['st_link']} / 찾은 링크 : {title.get_attribute('href')}")
                    if workInfo['st_link'] in title.get_attribute('href'):
                        title.click()
                        searchSuccess = True
                        wait_float(1.2,1.9)
                        break
            except:
                pg.moveTo(300,400)
                print('링크 클릭 안됨! 스크롤 올리기!')
                if oddCount % 2 == 0:
                    pg.scroll(200)
                else:
                    pg.scroll(-200)
            if searchSuccess == True:
                break
        if noSearchStatus == False:
            # noSearchStatus 가 False로 정상 작업 GOGO!!

            for k in range(scrollRanVal):
                pg.moveTo(300,400)
                pg.scroll(-150)
                if test == 'ok':
                    wait_float(0.1,0.4)
                else:
                    wait_float(2.5,3.5)

            if workInfo['st_addlink']:

                aTagClickSuccess = False
                oddCount = 0
                while True:
                    oddCount += 1
                    aTagList = driver.find_elements(by=By.CSS_SELECTOR, value="a")

                    try:
                        for aTag in aTagList:
                            print(aTag)
                            print(aTag.get_attribute('href'))
                            if aTag.get_attribute('href') is not None:
                                if workInfo['st_addlink'] in aTag.get_attribute('href'):
                                    aTag.click()
                                    aTagClickSuccess = True
                                    wait_float(1.2,1.9)
                                    break
                    except:
                        print('링크 클릭 안됨! 스크롤 올리기!')
                        if oddCount % 2 == 0:
                            pg.scroll(200)
                        else:
                            pg.scroll(-200)

                    try:
                        closeBtn = driver.find_element(by=By.CSS_SELECTOR, value=".btns .ButtonBase--gray")
                        closeBtn.click()
                    except:
                        pass

                    if aTagClickSuccess == True:
                        break

                driver.switch_to.window(driver.window_handles[1])
                for k in range(scrollRanVal):
                    pg.moveTo(300,400)
                    pg.scroll(-150)
                    if test == 'ok':
                        wait_float(0.1,0.4)
                    else:
                        wait_float(2.5,3.5)

        targetWorkStatus = True

    except Exception as e:
        print(e)
        targetWorkStatus = False
    
    return targetWorkStatus



# PC 버전 함수들!!!!!

def searchPcAnotherList(driver, workCount, test = None):
    errCount = 0
    onotherListStatus = True
    while True:
        errCount += 1
        print(errCount)
        if errCount > 6:
            onotherListStatus = False
            return
        if errCount > 3:
            focus_window('Chrome')
            pg.press('F5')
        print('타겟 외 클릭할 리스트 뽑기')
        wait_float(1.2,1.9)

        try:
            w1 = driver.find_elements(by=By.CSS_SELECTOR, value=".title_link")
        except:
            print('인기글 찾기 에러~')
            pass
        try:
            w2 = driver.find_elements(by=By.CSS_SELECTOR, value=".link_question")
        except:
            print('지식인 리스트 찾기 에러~')
            pass
        try:
            w3 = driver.find_elements(by=By.CSS_SELECTOR, value=".news_tit")
        except:
            print('뉴스글 찾기 에러~')
            pass

        try:
            w4 = driver.find_elements(by=By.CSS_SELECTOR, value=".fds-comps-right-image-text-content")
        except:
            print('기타 view 탭 컨텐츠 찾기 에러~')
            pass

        onotherList = w1 + w2 + w3 + w4
        if len(onotherList) > 0:
            break
    print('타겟 외 클릭할 리스트 뽑기 완료!!')

    wait_float(1.2,1.9)

    if onotherListStatus == True:
        try:
            print('onotherList 작업 GO')
            # 타겟 외 다른 포스팅 클릭하는 부분, 가끔 timeout이 발생하니 에러가 날 경우 돌아가기!
            ranNumCount = -1
            while True:

                print('여기서 도는건가??')
                if len(onotherList) < 2:
                    break

                wait_float(1.2,1.9)
                ranNumCount += 1
                if ranNumCount >= workCount:
                    break

                try:
                    wait_float(0.3,0.5)
                    print(f"onotherList 갯수는? : {len(onotherList)}")
                    workOnotherVal = random.randrange(0, len(onotherList) - 1)
                    wait_float(0.3,0.5)
                    forClickEle = onotherList.pop(workOnotherVal)
                    print(f'클릭할 other 타겟 제목은? {forClickEle.text}')

                    errCount = 0
                    errStatus = False
                    oddCount = 0
                    while True:
                        oddCount += 1
                        errCount += 1
                        if errCount > 10:
                            errStatus = True
                            break
                        try:
                            wait_float(0.3,0.5)
                            forClickEle.click()
                            break
                        except Exception as e:
                            print(str(e))
                            print('요소 클릭 실패 에러!! (해당 페이지는 검색창이 있는 화면이어야 함)')
                            print(forClickEle.text)
                            wait_float(0.3,0.5)
                            if oddCount % 2 == 0:
                                pg.scroll(200)
                            else:
                                pg.scroll(-200)

                    if errStatus == False:
                        scrollRanVal = random.randrange(5, 12)
                        for k in range(scrollRanVal):
                            
                            pg.moveTo(300,400)
                            pg.scroll(-150)
                            if test == 'ok':
                                wait_float(0.1,0.4)
                            else:
                                wait_float(2.5,3.5)
                            
                            
                except Exception as e:
                    print(str(e))
                    print('onotherList 를 못찾거나 하는 에러!!')
                    pg.press('F5')
                    pass

                driver.switch_to.window(driver.window_handles[0])
            pg.press('home')
        except Exception as e:
            print(e)
            print('타겟 클릭 실패! 넘어가기!')
            pass

def searchPcContent(driver, workInfo, workType, test = None):
    # targetWorkStatus 는 순위권 내에서 찾으면 True / 아니면 False를 리턴한다~
    targetWorkStatus = False

    # 먼저 메인에서 3번 찾아보기!
    errCount = 0
    while True:
        errCount += 1
        if errCount > 3:
            errCount = 0
            break
        wait_float(0.5,1.2)
        targetWorkStatus = searchContentInnerWork(driver, workInfo, workType, test)
        print(f'메인에서 클릭 또는 노출 확인 완료')
        if targetWorkStatus == True:
            return targetWorkStatus
    # 메인에서 못찾았을 경우 뒤로 가기
    # 먼저 더보기 or 2페이지 클릭

    errCount = 0
    while True:
        errCount += 1
        print('상세 페이지 노출되어 있는거 없음 검색결과 클릭 시작!')
        moreTabStatus = False
        wait_float(0.5,0.9)
        if errCount > 10:
            try:
                allTabBtn = driver.find_elements(by=By.CSS_SELECTOR, value=".api_flicking_wrap .flick_bx")
                allTabBtn[0].click()
            except:
                pass
        try:
            moreTab1 = driver.find_elements(by=By.CSS_SELECTOR, value=".group_more")
            moreTab2 = driver.find_elements(by=By.CSS_SELECTOR, value=".link_feed_more")
            moreTab = moreTab1 + moreTab2
            for more in moreTab:
                print(more.text)
                if '검색결과' in more.text:
                    moreTabStatus = True
                    more.click()
                    break

            if moreTabStatus == True:
                break
            else:
                pagingList = driver.find_elements(by=By.CSS_SELECTOR, value=".sc_page_inner .btn")
                for page in pagingList:
                    print(page.text)
                    if page.text == '2':
                        page.click()
                        moreTabStatus = True
                        break
                if moreTabStatus == True:
                    break
        except Exception as e:
            wait_float(0.5,0.9)
            print(str(e))
            print('검색창에서 "검색결과" 클릭 에러!')
            active_chrome(driver)
            focus_window('Chrome')
            pg.click(60,400)
            if errCount % 2 == 0:
                pg.press('end')
            else:
                pg.press('home')
            wait_float(0.5,0.9)
            pass
    

    # 검색결과 클릭 완료!!

    # 본격적으로 순위 찾는 부분!!
    scIdx = 2
    while True:
        scIdx += 1
        if scIdx > 11:
            # 10페이지 넘어가면 순위권에 없는거임 그럼 걍 리턴 쳐버리기~

            # 진짜 없는지 한번 체크하기!!!
            for i in range(3):
                fr = 1600    # range : 37 ~ 32767
                du = 500     # 1000 ms ==1second
                sd.Beep(fr, du)

            return targetWorkStatus

        targetWorkStatus = searchContentInnerWork(driver, workInfo, workType, test)
        if targetWorkStatus == True:
            return targetWorkStatus
        else:
            while True:
                try:
                    pagingList = driver.find_elements(by=By.CSS_SELECTOR, value=".sc_page_inner .btn")

                    wait_float(0.3,0.5)
                    for page in pagingList:
                        print(f"찾은 페이지 값은? {int(page.text)}")
                        print(f"l 값은?? {scIdx}")
                        if int(page.text) == scIdx:
                            page.click()
                            print(f"클릭한 페이지 값은? {int(scIdx)}")
                            break
                    break
                except Exception as e:
                    print(str(e))
                    print('검색결과 페이지 클릭 에러!')
                    pass



# 모바일 버전 함수들!!!!!!!!!!!!!!
def searchMobileAnotherList(driver, workCount, test = None):
    errCount = 0
    onotherListStatus = True
    while True:
        errCount += 1
        print(errCount)
        if errCount > 6:
            onotherListStatus = False
            return
        if errCount > 3:
            focus_window('Chrome')
            pg.press('F5')
        print('타겟 외 클릭할 리스트 뽑기')
        wait_float(1.2,1.9)

        try:
            w1 = driver.find_elements(by=By.CSS_SELECTOR, value=".title_link")
        except:
            print('viewtabList 찾기 에러~')
            pass
        try:
            w2 = driver.find_elements(by=By.CSS_SELECTOR, value=".fds-comps-right-image-text-title")
        except:
            print('viewtabList 찾기 에러~')
            pass
        try:
            w3 = driver.find_elements(by=By.CSS_SELECTOR, value=".question_text")
        except:
            print('viewtabList 찾기 에러~')
            pass

        try:
            w4 = driver.find_elements(by=By.CSS_SELECTOR, value=".tit_area")
        except:
            print('viewtabList 찾기 에러~')
            pass

        
        onotherList = w1 + w2 + w3 + w4
        if len(onotherList) > 0:
            break
    print('타겟 외 클릭할 리스트 뽑기 완료!!')

    wait_float(1.2,1.9)


    if onotherListStatus == True:
        try:
            print('onotherList 작업 GO')
            # 타겟 외 다른 포스팅 클릭하는 부분, 가끔 timeout이 발생하니 에러가 날 경우 돌아가기!
            ranNumCount = -1
            while True:
                if len(onotherList) < 2:
                    break

                wait_float(1.2,1.9)
                ranNumCount += 1
                if ranNumCount >= workCount:
                    break

                try:
                    wait_float(0.3,0.5)
                    print(f"onotherList 갯수는? : {len(onotherList)}")
                    workOnotherVal = random.randrange(0, len(onotherList) - 1)
                    wait_float(0.3,0.5)
                    forClickEle = onotherList.pop(workOnotherVal)
                    print(f'클릭할 other 타겟 제목은? {forClickEle.text}')

                    errCount = 0
                    errStatus = False
                    oddCount = 0
                    while True:
                        oddCount += 1
                        errCount += 1
                        if errCount > 10:
                            errStatus = True
                            break
                        try:
                            wait_float(0.3,0.5)
                            forClickEle.click()
                            break
                        except Exception as e:
                            print(str(e))
                            print('요소 클릭 실패 에러!! (해당 페이지는 검색창이 있는 화면이어야 함)')
                            print(forClickEle.text)
                            wait_float(0.3,0.5)
                            if oddCount % 2 == 0:
                                pg.scroll(200)
                            else:
                                pg.scroll(-200)

                    if errStatus == False:
                        scrollRanVal = random.randrange(5, 12)
                        for k in range(scrollRanVal):
                            
                            pg.moveTo(300,400)
                            if test == 'ok':
                                wait_float(0.1,0.4)
                            else:
                                wait_float(2.5,3.5)
                            pg.scroll(-150)
                            
                except Exception as e:
                    print(str(e))
                    print('onotherList 를 못찾거나 하는 에러!!')
                    pg.press('F5')
                    pass

                previousErrCount = 0
                while True:
                    print('여기서 도는거 같은데?!?!?!')
                    previousErrCount += 1
                    wait_float(1.2,1.9)
                    try:
                        script = """
                        var result = false;
                        if (window.history.forward() != null) {
                            result = true;
                        }
                        return result;
                        """
                        wait_float(0.5,1.2)
                        can_go_forward = driver.execute_script(script)
                        print(f"can_go_forward : {can_go_forward}")
                        wait_float(0.5,1.2)

                        if can_go_forward:
                            driver.forward()
                            driver.forward()
                        else:
                            # 귀찮다 두번하자 그냥~~~~~
                            driver.back()
                            wait_float(1.5,2.2)
                            current_url = driver.current_url

                            if "data:" in current_url:
                                wait_float(1.2,1.9)
                                driver.forward()
                                wait_float(1.2,1.9)
                                driver.forward()
                                continue
                            arrival = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")

                            print(f"current_url : {current_url}")
                            print(arrival)

                            if "search" in current_url and len(arrival) > 0:
                                print('검색 단계로 넘어옴!!!!!!!!')
                                break

                            # driver.back() 대신 물리적으로 클릭하기~~ (쿠팡 병신땜시)
                            pg.moveTo(30,65)
                            pg.click(30,65)
                            wait_float(1.5,2.2)
                            current_url = driver.current_url
                            arrival = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")

                            print(current_url)
                            print(arrival)

                            if "search" in current_url and len(arrival) > 0:
                                print('검색 단계로 넘어옴!!!!!!!!')
                                break

                    except Exception as e:
                        if previousErrCount > 5:
                            previousErrCount = 0
                            driver.forward()
                        print(str(e))
                        print('뒤로가기 후 검색창 있는곳에 도달 못하는 에러!!')
                        pass

                    try:
                        current_url = driver.current_url
                        if "chrome" in current_url:
                            driver.forward()
                            wait_float(1.2,1.9)
                            driver.forward()
                            wait_float(1.2,1.9)

                        current_url = driver.current_url
                        arrival = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")

                        if "search" in current_url and len(arrival) > 0:
                                print('검색 단계로 넘어옴!!!!!!!!')
                                break

                    except:
                        pass
            pg.press('home')
        except Exception as e:
            print(e)
            print('타겟 클릭 실패! 넘어가기!')
            pass

def goBackToMobileSearchTab(driver):
    while True:
        wait_float(1.2,1.9)
        try:
            script = """
            var result = false;
            if (window.history.forward() != null) {
                result = true;
            }
            return result;
            """
            wait_float(0.5,1.2)
            can_go_forward = driver.execute_script(script)
            print(can_go_forward)
            wait_float(0.5,1.2)

            if can_go_forward:
                driver.forward()
                driver.forward()
            else:
                # 귀찮다 두번하자 그냥~~~~~
                driver.back()
                wait_float(1.5,2.2)
                current_url = driver.current_url
                arrival = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")

                print(current_url)
                print(arrival)

                if "search" in current_url and len(arrival) > 0:
                    print('검색 단계로 넘어옴!!!!!!!!')
                    break

                # driver.back() 대신 물리적으로 클릭하기~~ (쿠팡 병신땜시)
                pg.moveTo(30,65)
                pg.click(30,65)
                wait_float(1.5,2.2)
                current_url = driver.current_url
                arrival = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")

                print(current_url)
                print(arrival)

                if "search" in current_url and len(arrival) > 0:
                    print('검색 단계로 넘어옴!!!!!!!!')
                    break
        except Exception as e:
            print(str(e))
            print('뒤로가기 후 검색창 있는곳에 도달 못하는 에러!!')
            pass

        try:
            current_url = driver.current_url
            if "chrome" in current_url:
                driver.forward()
                wait_float(1.2,1.9)
                driver.forward()
                wait_float(1.2,1.9)

            current_url = driver.current_url
            arrival = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")

            if "search" in current_url and len(arrival) > 0:
                    print('검색 단계로 넘어옴!!!!!!!!')
                    break

        except:
            pass

        try:
            wait_float(0.5,1.2)
            window_handles = driver.window_handles
            main_window = window_handles[0]
            for handle in window_handles:
                wait_float(0.3,0.9)
                if handle != main_window:
                    # 남기고 싶은 창이 아니면 닫기
                    driver.switch_to.window(handle)
                    driver.close()
                    
            driver.switch_to.window(main_window)
        except:
            pass
    
    pg.press('home')

def searchMobileContent(driver, workInfo, workType, test = None):
    # targetWorkStatus 는 순위권 내에서 찾으면 True / 아니면 False를 리턴한다~
    targetWorkStatus = False

    # 먼저 메인에서 3번 찾아보기!
    errCount = 0
    while True:
        errCount += 1
        if errCount > 3:
            errCount = 0
            break
        wait_float(0.5,1.2)
        targetWorkStatus = searchContentInnerWork(driver, workInfo, workType, test)
        if targetWorkStatus == True:
            return targetWorkStatus
    
    # 메인에서 못찾았을 경우 뒤로 가기
    # 먼저 더보기 or 2페이지 클릭

    errCount = 0
    while True:
        errCount += 1
        if errCount > 10:
            pg.press('home')
            errCount = 0
        print('상세 페이지 노출되어 있는거 없음 검색결과 클릭 시작!')
        moreTabStatus = False
        wait_float(0.5,0.9)
        try:
            moreTab1 = driver.find_elements(by=By.CSS_SELECTOR, value=".group_more")
            moreTab2 = driver.find_elements(by=By.CSS_SELECTOR, value=".link_feed_more")
            moreTab = moreTab1 + moreTab2
            for more in moreTab:
                print(more.text)
                if '검색결과' in more.text:
                    moreTabStatus = True
                    more.click()
                    break

            if moreTabStatus == True:
                break
            else:
                pagingList = driver.find_elements(by=By.CSS_SELECTOR, value=".pgn")
                for page in pagingList:
                    if page.text == '2':
                        page.click()
                        moreTabStatus = True
                        break
                if moreTabStatus == True:
                    break
        except Exception as e:
            wait_float(0.5,0.9)
            print('검색창에서 "검색결과" 클릭 에러!')
            active_chrome(driver)
            focus_window('Chrome')
            pg.press('end')
            pass
    

    # 검색결과 클릭 완료!!

    # 본격적으로 순위 찾는 부분!!
    scIdx = 2
    while True:
        scIdx += 1
        if scIdx > 11:
            # 10페이지 넘어가면 순위권에 없는거임 그럼 걍 리턴 쳐버리기~
            return targetWorkStatus

        targetWorkStatus = searchContentInnerWork(driver, workInfo, workType, test)
        if targetWorkStatus == True:
            return targetWorkStatus
        else:
            while True:
                try:
                    pagingList = driver.find_elements(by=By.CSS_SELECTOR, value=".pgn")

                    wait_float(0.3,0.5)
                    for page in pagingList:
                        print(f"찾은 페이지 값은? {int(page.text)}")
                        print(f"l 값은?? {scIdx}")
                        if int(page.text) == scIdx:
                            page.click()
                            print(f"클릭한 페이지 값은? {int(scIdx)}")
                            break
                    break
                except Exception as e:
                    print(str(e))
                    print('검색결과 페이지 클릭 에러!')
                    pass



# 모바일 / PC 공통 함수!!!!!!!!!!!!!!!!

def naverMainSearch(driver, searchTxt, workDevice):
    print(searchTxt)
    errCount = 0
    while True:
        wait_float(0.3,0.8)
        print('현재 창 1번인지 체크!!')
        try:
            nowActiveWindowIndex = get_active_window_index(driver)
            if nowActiveWindowIndex == 0:
                break
            else:
                pg.press('enter')
                driver.switch_to.window(driver.window_handles[0]) 
        except:
            pass






    while True:
        errCount += 1
        print(f"네이버 서치 에러 카운트는? {errCount}")
        if errCount > 7:
            focus_window('Chrome')
            pg.press('F5')
        if errCount > 10:
            return False
        
        pg.click(40,250)
        try:
            wait_float(0.5,0.8)
            mainSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#MM_SEARCH_FAKE")
            mainSearchTab.click()
        except Exception as e:
            # print(str(e))
            pass

        try:
            wait_float(0.5,0.8)
            subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#query")
            subSearchTab.click()
        except Exception as e:
            # print(str(e))
            pass

        try:
            wait_float(0.5,0.8)
            subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#nx_query")
            subSearchTab.click()
        except Exception as e:
            # print(str(e))
            pass

        try:
            pg.hotkey('ctrl', 'a')
            pg.press('delete')
            wait_float(1.2,1.9)
            cb.copy(searchTxt)
            pg.hotkey('ctrl', 'v')
            wait_float(1.2,1.9)
        except:
            pass

        print('검색까지는 완료!!')

        
        try:
            subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#query")
            searchVal = subSearchTab.get_attribute('value')
            if searchVal is not None and searchVal == searchTxt:
                pg.press('enter')
        except Exception as e:
            # print(str(e))
            pass

        try:
            subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#nx_query")
            searchVal = subSearchTab.get_attribute('value')
            if searchVal is not None and searchVal == searchTxt:
                pg.press('enter')
        except Exception as e:
            # print(str(e))
            pass

        if workDevice == 'mobile':
            try:
                wait_float(1.5,2.2)
                subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#query")
                searchVal = subSearchTab.get_attribute('value')
                if searchVal == searchTxt:
                    break
            except Exception as e:
                # print(str(e))
                pass

            try:
                wait_float(1.5,2.2)
                subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#nx_query")
                searchVal = subSearchTab.get_attribute('value')
                if searchVal == searchTxt:
                    break
            except Exception as e:
                # print(str(e))
                pass
        else:
            try:
                wait_float(1.5,2.2)
                successSearchEle = driver.find_elements(by=By.CSS_SELECTOR, value=".lnb_group")
                subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#query")
                searchVal = subSearchTab.get_attribute('value')
                if len(successSearchEle) > 0 and searchVal == searchTxt:
                    break
            except Exception as e:
                # print(str(e))
                pass

            try:
                wait_float(1.5,2.2)
                successSearchEle = driver.find_elements(by=By.CSS_SELECTOR, value=".lnb_group")
                subSearchTab = driver.find_element(by=By.CSS_SELECTOR, value="#nx_query")
                searchVal = subSearchTab.get_attribute('value')
                if len(successSearchEle) > 0 and searchVal == searchTxt:
                    break
            except Exception as e:
                # print(str(e))
                pass

def searchContentInnerWork(driver, workInfo, workType, test):
    targetWorkStatus = False
    try:
        targetList = driver.find_elements(by=By.CSS_SELECTOR, value=".rdmOs_JPV27pWNOhAhxL")
        actTarget = ""
        for target in targetList:
            getHref = target.get_attribute('href')
            st_link = str(workInfo['st_link']).strip()
            getHref = getHref.strip()

            print(st_link)
            print(getHref)

            wait_float(0.1,0.3)
            if workInfo['st_same_link']:
                if st_link == getHref:
                    print('여기까지 왔다!!')
                    actTarget = target
                    # workInfo['work_type'] 이 클릭이면 클릭 / 아니면 그냥 해당 위치로 스크롤만 하고 패스~
                    targetWorkStatus = True
                    break
            else:
                if st_link in getHref:
                    actTarget = target
                    # workInfo['work_type'] 이 클릭이면 클릭 / 아니면 그냥 해당 위치로 스크롤만 하고 패스~
                    targetWorkStatus = True
                    break


                
        print('나와야지 ㅠㅠㅠ')
        if targetWorkStatus == True:
            wait_float(1.2,1.5)
            browserMiddleMoveJsCode = """
            var element = arguments[0];
            var elementRect = element.getBoundingClientRect();
            var absoluteElementTop = elementRect.top + window.pageYOffset;
            var middle = absoluteElementTop - (window.innerHeight / 2);
            window.scrollTo({ top: middle, behavior: 'smooth'});
            """
            driver.execute_script(browserMiddleMoveJsCode, actTarget)
            wait_float(1.2,1.5)
            print('위치로 갔다잉~')

            if workInfo['work_type'] == 'click':

                # 먼저 타겟 클릭하기~
                errCount = 0
                while True:
                    errCount += 1
                    print(errCount)
                    if errCount > 5:
                        print('break 들어옴!!!')
                        mobileChk = driver.find_elements(by=By.CSS_SELECTOR, value=".logo_naver")
                        pcChk = driver.find_elements(by=By.CSS_SELECTOR, value="#nx_query")
                        if len(mobileChk) == 0 and len(pcChk) == 0:
                            break
                        else:
                            errCount = 0
                    print('타겟 클릭~')
                    try:
                        actTarget.click()
                        break
                    except:
                        wait_float(0.5,1.2)
                        pg.scroll(-150)
                        pass

                # 내리면서 스크롤 하기
                scrollRanVal = random.randrange(8, 15)
                for k in range(scrollRanVal):
                    pg.moveTo(300,400)
                    pg.scroll(-150)
                    if test == 'ok':
                        wait_float(0.1,0.5)
                    else:
                        wait_float(5.5,7.5)
                
                if workInfo['st_addlink']:
                    targetLink = workInfo['st_addlink']
                    focus_window('Chrome')
                    wait_float(0.3,0.5)
                    pg.press('home')

                    innerLinkWorkStatus = False
                    while True:
                        innerLinkList = driver.find_elements(by=By.CSS_SELECTOR, value="a")
                        wait_float(0.1,0.2)
                        for aTag in innerLinkList:
                            try:
                                getAtagHref = aTag.get_attribute('href')
                                if getAtagHref is None:
                                    continue

                                if targetLink in getAtagHref or targetLink == getAtagHref:
                                    while True:
                                        try:
                                            pg.moveTo(300,400)
                                            wait_float(1.2,1.9)
                                            pg.scroll(-200)
                                            wait_float(1.2,1.9)
                                            aTag.click()
                                            innerLinkWorkStatus = True
                                            break
                                        except Exception as e:
                                            print(e)
                                            pass

                                    scrollRanVal = random.randrange(5, 12)
                                    for k in range(scrollRanVal):
                                        pg.moveTo(300,400)
                                        pg.scroll(-150)
                                        if test == 'ok':
                                            wait_float(0.1,0.5)
                                        else:
                                            wait_float(5.5,7.5)
                                    break
                            except:
                                pass
                        if innerLinkWorkStatus:
                            break
                if workType['pr_work_type'] == 'mobile':
                    goBackToMobileSearchTab(driver)
                else:
                    driver.switch_to.window(driver.window_handles[0])

            # 여기서 작업 하고 targetWorkStatus True로 변경
        

        print(f"targetWorkStatus : {targetWorkStatus}")
        return targetWorkStatus
    except Exception as e:
        print(str(e))
        pass


# 한 브라우저에 여러개 창이 열려있을경우 현재 창이 몇번째인지 확인하는 함수
def get_active_window_index(driver):
    current_window_handle = driver.current_window_handle
    all_window_handles = driver.window_handles
    return all_window_handles.index(current_window_handle)