# func.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import load_workbook
import pyautogui as pg
import random

def wait_ready(driver, timeout=15):
    """
    문서 readyState가 'complete'가 될 때까지 대기.
    """
    end = time.time() + timeout
    while time.time() < end:
        try:
            if driver.execute_script("return document.readyState") == "complete":
                return True
        except Exception:
            pass
        time.sleep(0.1)
    return False

def wait_visible(driver, locator, timeout=10):
    """
    특정 요소가 보일 때까지 대기.
    locator 예: (By.CSS_SELECTOR, "input[name='q']")
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def band_join_loop(driver, cancel_event, stop_event):
    print('밴드 가입 들어옴!!!!')

    bandWb = load_workbook('./etc/blog_work.xlsx')
    bandEx = bandWb.active

    try:
        with open(f'./etc/profile.txt', 'rt', encoding='UTF8') as f:
            profile = f.read()
    except:
        pass

    try:
        with open(f'./etc/profile.txt', 'r') as f:
            profile = f.read()
    except:
        pass

    if profile == '':
        pg.alert('프로필이 비어있습니다. profile.txt 파일을 확인해주세요.')
        return

    bandCount = 1
    while not cancel_event.is_set() and not stop_event.is_set():

        bandCount += 1
        if bandEx.cell(bandCount,1).value is None:
            break

        print(bandEx.cell(bandCount,1).value)

        url = bandEx.cell(bandCount,1).value
        driver.get(url)

        _btnJoinBand

        # lyContent << 이게 가입 팝업창

        # 밴드 가입 창 열기


        
        pass

def band_write_loop(
    driver,
    cancel_event,
    stop_event,
    step=800,
    interval=0.3,
    loop_top=True,
    max_idle_rounds=8,
):
    """
    네이버 페이지에서 반복 스크롤.
    - cancel_event.set() → 현재 작업만 중단(브라우저 유지)
    - stop_event.set()   → 전체 종료 흐름에 따라 루프 탈출
    - 바닥에 도달해 더 이상 높이가 늘지 않으면 idle 카운트 증가,
      max_idle_rounds에 도달 시 맨 위로 올려 반복(loop_top=True) 또는 대기.
    """
    driver.get('https://band.us')
    wait_ready(driver)

    idle = 0
    while not cancel_event.is_set() and not stop_event.is_set():
        pass





# -----------------------------------------------------

def wait_float(start, end):
    wait_ran = random.uniform(start, end)
    time.sleep(wait_ran)