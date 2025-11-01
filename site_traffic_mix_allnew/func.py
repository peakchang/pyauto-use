import random
import threading
from datetime import datetime
import sys
import tempfile, shutil, psutil, subprocess, os, time
from ppadb.client import Client as AdbClient
import requests
import clipboard as cb
import pyautogui as pg

import ctypes
import pygetwindow as gw
from pywinauto import Desktop

from tkinter import *
import tkinter as tk
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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


def focus_window(winNames):
    try:
        user32 = ctypes.windll.user32
        foreground_window = user32.GetForegroundWindow()
        window = gw.Window(foreground_window)
        chkDriver = False

        print(winNames)
        for winName in winNames:
            print(window.title)
            if winName in window.title:
                chkDriver = True
                break
            else:
                windows = Desktop(backend="uia").windows()
                for window in windows:
                    if winName in window.window_text():
                        window.set_focus()
                        break
        return chkDriver
            

    except Exception as e:
        print(str(e))
        pass






def focus_window_and_tab(driver, winNames):
    try:
        user32 = ctypes.windll.user32
        foreground_window = user32.GetForegroundWindow()
        gw_window = gw.Window(foreground_window)
        chkDriver = False
        
        print(f"Finding windows/tabs: {winNames}")
        
        for winName in winNames:
            # 1단계: 현재 포그라운드 윈도우 확인
            print(f"Current foreground: {gw_window.title}")
            if winName in gw_window.title:
                chkDriver = True
                # Selenium 탭도 확인
                check_and_switch_tab(driver, winName)
                break
            else:
                # 2단계: 다른 윈도우 찾기
                windows = Desktop(backend="uia").windows()
                window_found = False
                
                for uia_window in windows:
                    if winName in uia_window.window_text():
                        uia_window.set_focus()
                        time.sleep(0.3)  # 포커스 전환 대기
                        window_found = True
                        chkDriver = True
                        break
                
                if window_found:
                    # 윈도우를 찾았으면 해당 윈도우의 Selenium 탭도 확인
                    check_and_switch_tab(driver, winName)
                    break
        
        return chkDriver
            
    except Exception as e:
        print(f"Error in focus_window_and_tab: {str(e)}")
        return False


def check_and_switch_tab(driver, target_name):
    """
    Selenium driver의 모든 탭을 확인하고 
    target_name이 포함된 탭으로 전환
    """
    try:
        current_window = driver.current_window_handle
        all_windows = driver.window_handles
        
        print(f"Total tabs: {len(all_windows)}")
        
        # 모든 탭 순회
        for window_handle in all_windows:
            driver.switch_to.window(window_handle)
            time.sleep(0.1)  # 탭 전환 대기
            
            current_title = driver.title
            print(f"Checking tab: {current_title}")
            
            # 원하는 탭 찾으면 해당 탭에 머물기
            if target_name in current_title:
                print(f"✓ Switched to tab: {current_title}")
                return True
        
        # 찾지 못하면 원래 탭으로 복귀
        driver.switch_to.window(current_window)
        print(f"Target tab not found, stayed at: {driver.title}")
        return False
        
    except Exception as e:
        print(f"Error in check_and_switch_tab: {str(e)}")
        return False
    



def create_active_array(lengthArr, innerArr):
    # 배열의 길이는 랜덤한 값을 사용
    length = random.randint(lengthArr[0], lengthArr[1])
    
    # 기본적으로 모두 'notWork'로 채운다
    array = ['notWork'] * length
    
    # 첫 번째와 마지막 요소는 'notWork'로 유지
    array[0] = 'notWork'
    array[-1] = 'notWork'
    
    # 'work'의 개수를 랜덤으로 결정
    num_of_works = random.randint(innerArr[0], innerArr[1])
    
    # 첫 번째와 마지막 요소를 제외한 인덱스 리스트
    available_positions = list(range(1, length - 1))
    
    # 무작위로 num_of_works개의 위치를 선택하여 'work'로 설정
    work_positions = random.sample(available_positions, num_of_works)
    
    for pos in work_positions:
        array[pos] = 'work'
    
    # 'work' 위치 중 하나를 선택하여 'realwork'로 변경
    if work_positions:  # work_positions가 비어 있지 않은지 확인
        realwork_position = random.choice(work_positions)
        array[realwork_position] = 'realwork'
    
    return array

def create_active_array_many(lengthArr, innerArr, num_realworks=1):
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