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
from pywinauto.application import Application
from tkinter import *
import tkinter as tk
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def changeIp():
    getIp = ""
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
        success, res = request_safely_get("https://api.ip.pe.kr/json/")
        return res['ip']
    except Exception as e:
        pass




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


def focus_target_chrome(driver, title_parts):
    """
    driver: selenium webdriver (Chrome)
    title_parts: ['네이버', '검색'] 처럼 '모두' 포함돼야 매칭

    동작:
    1. selenium이 열어둔 창/탭 중에서 title_parts 전부 들어간 창 찾기
    2. 찾으면 그 창으로 switch
    3. OS 레벨에서 그 크롬 창에 포커스 맞춤
    4. 그 창을 제외한 '다른 크롬 창'은 전부 닫음 (사람이 연 크롬도 포함)
    5. 성공하면 True, 없으면 False
    """
    target_handle, target_title = _find_driver_window(driver, title_parts)
    if not target_handle:
        return False

    # 2) selenium 내부 포커스
    driver.switch_to.window(target_handle)

    # 3~4) OS 레벨 처리
    _focus_and_close_other_chromes(target_title)

    return True


def _find_driver_window(driver, title_parts):
    """
    Selenium이 관리하는 window_handles 중에서 title_parts 전부 포함하는 창 찾기
    """
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        title = (driver.title or "").strip()
        if all(part in title for part in title_parts):
            return handle, title
    return None, None


def _focus_and_close_other_chromes(target_title: str) -> None:
    """
    pywinauto로 떠 있는 크롬 창들을 순회해서
    - target_title 이 들어간 크롬은 살리고 포커스
    - 나머지 크롬은 전부 닫는다
    """
    try:
        from pywinauto import Desktop
    except ImportError:
        # pywinauto 없으면 OS 레벨 처리는 패스
        return

    desktop = Desktop(backend="uia")

    target_win = None
    windows = desktop.windows()

    # 1) 먼저 '살릴' 크롬 찾기
    for w in windows:
        wt = w.window_text()
        # 크롬 판별을 너무 빡세게 하면 안 되니까 느슨하게
        if ('Chrome' in wt or 'Google Chrome' in wt) and target_title in wt:
            target_win = w
            break

    # 포커스 먼저
    if target_win is not None:
        try:
            target_win.set_focus()
        except Exception:
            pass

    # 2) 이제 다른 크롬 창들 닫기
    for w in windows:
        wt = w.window_text()
        # 크롬 아니면 스킵
        if not ('Chrome' in wt or 'Google Chrome' in wt):
            continue

        # 내가 살리기로 한 창이면 스킵
        if target_win is not None and w.handle == target_win.handle:
            continue

        # 여기까지 왔으면 닫아도 되는 크롬
        try:
            w.close()
        except Exception:
            # 어떤 창은 닫기 막혀있을 수 있음 → 무시
            pass

# def focus_window(winNames):
#     try:
#         user32 = ctypes.windll.user32
#         foreground_window = user32.GetForegroundWindow()
#         window = gw.Window(foreground_window)
#         chkDriver = False

#         print(winNames)
#         for winName in winNames:
#             print(window.title)
#             if winName in window.title:
#                 chkDriver = True
#                 break
#             else:
#                 windows = Desktop(backend="uia").windows()
#                 for window in windows:
#                     if winName in window.window_text():
#                         window.set_focus()
#                         break
#         return chkDriver
            

#     except Exception as e:
#         print(str(e))
#         pass


# def focus_chrome_window_and_tab(driver, winNames):
#     """
#     크롬 창을 찾아서 활성화하고, winNames의 모든 키워드를 포함한 탭으로 전환
#     """
#     try:
#         if isinstance(winNames, str):
#             winNames = [winNames]
        
#         print(f"[INFO] Finding Chrome with ALL keywords: {winNames}")
        
#         # 1단계: 현재 포커스된 창이 Chrome인지 확인
#         is_chrome_focused = check_if_chrome_focused()
        
#         if not is_chrome_focused:
#             print("[INFO] 현재 Chrome 창이 아님 → Chrome 창 활성화 시도...")
            
#             # 여러 방법으로 Chrome 활성화 시도
#             chrome_activated = activate_chrome_window()
            
#             if not chrome_activated:
#                 print("[ERROR] ❌ Chrome 창을 활성화하지 못했습니다")
#                 print("[RESULT] Chrome 창 활성화 실패 → return False")
#                 return False
#         else:
#             print("[INFO] ✅ 이미 Chrome 창이 포커스되어 있음")
        
#         print("[CHECK] Chrome 창 활성화 상태: ✅ 성공")
        
#         # 2단계: 탭 찾기
#         time.sleep(0.5)  # 안정화 대기
        
#         print("[INFO] 이제 탭 검색 시작...")
#         tab_found = check_and_switch_tab_all_keywords(driver, winNames)
        
#         if tab_found:
#             print("[RESULT] ✅✅ Chrome 창 활성화 성공 + 탭 찾기 성공 → return True")
#             return True
#         else:
#             print("[RESULT] ✅❌ Chrome 창 활성화 성공 BUT 탭 찾기 실패 → return False")
#             return False
            
#     except Exception as e:
#         print(f"[ERROR] focus_chrome_window_and_tab 오류: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return False


# def check_if_chrome_focused():
#     """현재 포커스된 창이 Chrome인지 확인"""
#     try:
#         user32 = ctypes.windll.user32
#         foreground_window = user32.GetForegroundWindow()
#         gw_window = gw.Window(foreground_window)
#         title = gw_window.title
        
#         print(f"[INFO] 현재 포커스 창: {title}")
        
#         is_chrome = "Chrome" in title or "chrome" in title.lower()
#         return is_chrome
#     except:
#         return False


# def activate_chrome_window():
#     """여러 방법으로 Chrome 창 활성화 시도"""
    
#     # 방법 1: pygetwindow로 찾기
#     print("\n[방법 1] pygetwindow로 Chrome 창 찾기...")
#     try:
#         all_windows = gw.getAllTitles()
#         print(f"  → 총 {len(all_windows)}개 창 발견")
        
#         for title in all_windows:
#             if "Chrome" in title and title.strip():  # 빈 제목 제외
#                 print(f"  → Chrome 창 발견: {title}")
#                 try:
#                     chrome_win = gw.getWindowsWithTitle(title)[0]
#                     chrome_win.activate()
#                     time.sleep(0.5)
                    
#                     # 활성화 확인
#                     if check_if_chrome_focused():
#                         print(f"  ✅ [방법 1] 성공!")
#                         return True
#                 except Exception as e:
#                     print(f"  ✗ 활성화 실패: {str(e)}")
#                     continue
#     except Exception as e:
#         print(f"  ✗ [방법 1] 실패: {str(e)}")
    
#     # 방법 2: pywinauto Desktop으로 찾기
#     print("\n[방법 2] pywinauto Desktop으로 Chrome 창 찾기...")
#     try:
#         windows = Desktop(backend="uia").windows()
#         print(f"  → 총 {len(windows)}개 창 검색 중...")
        
#         for uia_window in windows:
#             try:
#                 window_title = uia_window.window_text()
                
#                 if "Chrome" in window_title or "Google Chrome" in window_title:
#                     print(f"  → Chrome 창 발견: {window_title}")
                    
#                     # 최소화 해제
#                     try:
#                         if uia_window.is_minimized():
#                             print(f"  → 최소화 상태 → 복원 중...")
#                             uia_window.restore()
#                             time.sleep(0.3)
#                     except:
#                         pass
                    
#                     # 포커스 설정
#                     uia_window.set_focus()
#                     time.sleep(0.5)
                    
#                     # 활성화 확인
#                     if check_if_chrome_focused():
#                         print(f"  ✅ [방법 2] 성공!")
#                         return True
#             except Exception as e:
#                 continue
#     except Exception as e:
#         print(f"  ✗ [방법 2] 실패: {str(e)}")
    
#     # 방법 3: win32gui로 강제 활성화
#     print("\n[방법 3] win32gui로 Chrome 창 강제 활성화...")
#     try:
#         import win32gui
#         import win32con
        
#         def enum_windows_callback(hwnd, results):
#             if win32gui.IsWindowVisible(hwnd):
#                 title = win32gui.GetWindowText(hwnd)
#                 if "Chrome" in title:
#                     results.append((hwnd, title))
        
#         chrome_windows = []
#         win32gui.EnumWindows(enum_windows_callback, chrome_windows)
        
#         print(f"  → {len(chrome_windows)}개 Chrome 창 발견")
        
#         for hwnd, title in chrome_windows:
#             print(f"  → 시도: {title}")
#             try:
#                 # 최소화 해제
#                 if win32gui.IsIconic(hwnd):
#                     win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
#                     time.sleep(0.3)
                
#                 # 맨 앞으로 가져오기
#                 win32gui.SetForegroundWindow(hwnd)
#                 time.sleep(0.5)
                
#                 # 활성화 확인
#                 if check_if_chrome_focused():
#                     print(f"  ✅ [방법 3] 성공!")
#                     return True
#             except Exception as e:
#                 print(f"  ✗ 실패: {str(e)}")
#                 continue
#     except ImportError:
#         print(f"  ✗ [방법 3] pywin32 미설치")
#     except Exception as e:
#         print(f"  ✗ [방법 3] 실패: {str(e)}")
    
#     # 방법 4: Alt+Tab 시뮬레이션
#     print("\n[방법 4] 키보드 입력으로 Chrome 창 찾기...")
#     try:
#         import pyautogui
        
#         # 현재 열린 모든 창 제목 가져오기
#         all_windows = gw.getAllTitles()
#         chrome_windows = [w for w in all_windows if "Chrome" in w and w.strip()]
        
#         if chrome_windows:
#             print(f"  → Chrome 창 {len(chrome_windows)}개 발견")
            
#             # Alt+Tab으로 전환 시도
#             for _ in range(len(all_windows)):
#                 pyautogui.keyDown('alt')
#                 pyautogui.press('tab')
#                 time.sleep(0.2)
#                 pyautogui.keyUp('alt')
#                 time.sleep(0.3)
                
#                 if check_if_chrome_focused():
#                     print(f"  ✅ [방법 4] 성공!")
#                     return True
#     except ImportError:
#         print(f"  ✗ [방법 4] pyautogui 미설치")
#     except Exception as e:
#         print(f"  ✗ [방법 4] 실패: {str(e)}")
    
#     print("\n❌ 모든 방법 실패")
#     return False


# def check_and_switch_tab_all_keywords(driver, target_keywords):
#     """모든 target_keywords를 포함한 탭으로 전환"""
#     try:
#         if isinstance(target_keywords, str):
#             target_keywords = [target_keywords]
        
#         current_window = driver.current_window_handle
#         all_windows = driver.window_handles
        
#         print(f"[TAB] 총 {len(all_windows)}개 탭 확인 중...")
#         print(f"[TAB] 필수 키워드 (모두 포함 필요): {target_keywords}")
        
#         for idx, window_handle in enumerate(all_windows):
#             try:
#                 driver.switch_to.window(window_handle)
#                 time.sleep(0.1)
                
#                 current_title = driver.title
#                 print(f"\n[TAB {idx+1}/{len(all_windows)}] 확인: {current_title}")
                
#                 all_keywords_found = True
#                 matched_keywords = []
#                 missing_keywords = []
                
#                 for keyword in target_keywords:
#                     if keyword in current_title:
#                         print(f"  ✓ '{keyword}' 포함됨")
#                         matched_keywords.append(keyword)
#                     else:
#                         print(f"  ✗ '{keyword}' 없음")
#                         missing_keywords.append(keyword)
#                         all_keywords_found = False
                
#                 if all_keywords_found:
#                     print(f"\n[TAB SUCCESS] ✓✓✓ 매칭 성공!")
#                     print(f"  → 모든 키워드 포함: {matched_keywords}")
#                     print(f"  → 탭 제목: '{current_title}'")
#                     return True
#                 else:
#                     print(f"  → 탈락 (누락된 키워드: {missing_keywords})")
                
#             except Exception as e:
#                 print(f"[TAB WARNING] 탭 {idx+1} 확인 실패: {str(e)}")
#                 continue
        
#         print(f"\n[TAB FAIL] ❌ 모든 키워드를 포함한 탭을 찾지 못했습니다")
        
#         try:
#             driver.switch_to.window(current_window)
#         except:
#             pass
        
#         return False
        
#     except Exception as e:
#         print(f"[ERROR] check_and_switch_tab_all_keywords 오류: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         return False


# # ===== 디버깅 함수 =====

# def debug_all_windows():
#     """시스템의 모든 창 출력 (디버깅용)"""
#     print("\n" + "="*70)
#     print("🔍 시스템의 모든 창 목록:")
#     print("="*70)
    
#     try:
#         all_titles = gw.getAllTitles()
#         chrome_count = 0
        
#         for idx, title in enumerate(all_titles):
#             if title.strip():  # 빈 제목 제외
#                 is_chrome = "Chrome" in title
#                 marker = " ← Chrome!" if is_chrome else ""
#                 print(f"{idx+1}. {title}{marker}")
#                 if is_chrome:
#                     chrome_count += 1
        
#         print(f"\n총 {len(all_titles)}개 창 중 Chrome: {chrome_count}개")
#     except Exception as e:
#         print(f"오류: {str(e)}")
    
#     print("="*70 + "\n")
    



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




def request_safely_get(site_link: str, timeout: int = 10, retry_delay: int = 3, max_retries: int = None):
    """
    서버에서 not work 정보를 안전하게 로드하는 함수
    
    Args:
        site_link: API 서버 링크
        timeout: 요청 타임아웃 (초)
        retry_delay: 재시도 대기 시간 (초)
        max_retries: 최대 재시도 횟수 (None이면 무제한)
    
    Returns:
        Tuple[bool, dict]: (성공여부, 응답데이터)
    """
    retry_count = 0
    
    while True:
        try:
            print('요청 시작!!')
            
            # 타임아웃 설정으로 무한 대기 방지
            response = requests.get(
                site_link,
                timeout=timeout
            )
            
            # HTTP 상태 코드 확인
            response.raise_for_status()
            
            # JSON 파싱
            res = response.json()
            print('요청 완료!')
            print(res)
            
            # status 또는 result가 True인지 확인
            status_ok = res.get('status') == True
            result_ok = res.get('result') == True
            
            if status_ok or result_ok:
                return (True, res)
            else:
                # 둘 다 False면 재시도
                print(f'status와 result가 모두 False입니다. {retry_delay}초 후 재시도...')
                time.sleep(retry_delay)
                continue
                
        except requests.exceptions.Timeout:
            print(f'타임아웃 발생! {retry_delay}초 후 재시도...')
            
        except requests.exceptions.ConnectionError:
            print(f'연결 오류 발생! {retry_delay}초 후 재시도...')
            
        except requests.exceptions.HTTPError as e:
            print(f'HTTP 오류 발생: {e}. {retry_delay}초 후 재시도...')
            
        except requests.exceptions.RequestException as e:
            print(f'요청 오류 발생: {e}. {retry_delay}초 후 재시도...')
            
        except ValueError as e:
            print(f'JSON 파싱 오류: {e}. {retry_delay}초 후 재시도...')
            
        except Exception as e:
            print(f'예상치 못한 오류 발생: {str(e)}. {retry_delay}초 후 재시도...')
        
        # 재시도 카운트 증가
        retry_count += 1
        if max_retries is not None and retry_count >= max_retries:
            print(f'최대 재시도 횟수({max_retries})에 도달했습니다.')
            return (False, {})
        
        # 재시도 전 대기
        time.sleep(retry_delay)



def load_notwork_safely_post(site_link: str, data = None, timeout: int = 10, retry_delay: int = 3, max_retries: int = None):
    """
    서버에서 not work 정보를 안전하게 로드하는 함수 (POST 버전)
    
    Args:
        site_link: API 서버 링크
        data: POST 요청에 포함할 데이터 (dict)
        timeout: 요청 타임아웃 (초)
        retry_delay: 재시도 대기 시간 (초)
        max_retries: 최대 재시도 횟수 (None이면 무제한)
    
    Returns:
        Tuple[bool, dict]: (성공여부, 응답데이터)
    """
    retry_count = 0
    
    if data is None:
        data = {}
    
    while True:
        try:
            print('not work 불러와야지?!')
            
            # 타임아웃 설정으로 무한 대기 방지
            response = requests.post(
                f"{site_link}/api/v7/res_traffic_work/load_notwork",
                json=data,
                timeout=timeout
            )
            
            # HTTP 상태 코드 확인
            response.raise_for_status()
            
            # JSON 파싱
            res = response.json()
            print('now work 정보!')
            print(res)
            
            # status 키가 있는지 확인
            if 'status' not in res:
                print('경고: status 키가 응답에 없습니다.')
                time.sleep(retry_delay)
                continue
            
            # status가 True일 때만 성공으로 처리
            if res['status'] == True:
                return (True, res)
            else:
                # status가 False면 재시도
                print(f'status가 False입니다. {retry_delay}초 후 재시도...')
                time.sleep(retry_delay)
                continue
                
        except requests.exceptions.Timeout:
            print(f'타임아웃 발생! {retry_delay}초 후 재시도...')
            
        except requests.exceptions.ConnectionError:
            print(f'연결 오류 발생! {retry_delay}초 후 재시도...')
            
        except requests.exceptions.HTTPError as e:
            print(f'HTTP 오류 발생: {e}. {retry_delay}초 후 재시도...')
            
        except requests.exceptions.RequestException as e:
            print(f'요청 오류 발생: {e}. {retry_delay}초 후 재시도...')
            
        except ValueError as e:
            print(f'JSON 파싱 오류: {e}. {retry_delay}초 후 재시도...')
            
        except Exception as e:
            print(f'예상치 못한 오류 발생: {str(e)}. {retry_delay}초 후 재시도...')
        
        # 재시도 카운트 증가
        retry_count += 1
        if max_retries is not None and retry_count >= max_retries:
            print(f'최대 재시도 횟수({max_retries})에 도달했습니다.')
            return (False, {})
        
        # 재시도 전 대기
        time.sleep(retry_delay)





class HistoryTracker:
    def __init__(self):
        self.history_count = 0
        self.current_position = 0
    
    def record_navigation(self):
        """페이지 이동 시 호출"""
        self.history_count += 1
        self.current_position = self.history_count
        print(f"[INFO] 히스토리 기록: {self.current_position}/{self.history_count}")
    
    def record_back(self):
        """뒤로가기 시 호출"""
        if self.current_position > 1:
            self.current_position -= 1
        print(f"[INFO] 뒤로가기: {self.current_position}/{self.history_count}")
        return self.can_go_back()
    
    def can_go_back(self):
        """뒤로갈 수 있는지 확인"""
        return self.current_position > 1
    
    def back_count_available(self):
        """뒤로갈 수 있는 횟수"""
        return self.current_position - 1