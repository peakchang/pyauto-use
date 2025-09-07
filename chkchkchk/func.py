# func.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

def naver_scroll_loop(
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