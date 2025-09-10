# action.py
import threading
import queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import pyautogui as pg
import clipboard as cb
import os

from func import band_write_loop, band_join_loop, time, wait_float, focus_window

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

class BrowserWorker:
    """
    - 단일 Selenium 드라이버(브라우저) 생성/보유
    - cancel_event: 현재 실행중인 작업만 중단
    - stop_event: 전체 종료
    - busy: '길게 도는 작업' 실행 중인지 표시 (중복 실행 방지용)
    - scroll_pending: 네이버 스크롤이 큐에 '대기 중'인지 표시 (중복 큐잉 방지)
    - on_message: UI에 스레드 안전하게 메시지 전달하는 콜백 (root.after로 구현)
    """
    def __init__(self, headless=False, on_message=None):
        self.cmd_q = queue.Queue()
        self.stop_event = threading.Event()
        self.cancel_event = threading.Event()
        self.busy = threading.Event()
        self.scroll_pending = False
        self.join_pending = False

        self.thread = None
        self.driver = None
        self.headless = headless
        self.on_message = on_message

        self.driver_ready = threading.Event()   # _make_driver 끝났는지
        self.making_driver = threading.Event()  # 만들고 있는 중인지

    # ===== 내부 유틸 =====
    def _notify(self, msg: str):
        if self.on_message:
            try:
                self.on_message(msg)
            except Exception:
                pass

    # ===== 생명주기 =====
    def start(self):
        if self.thread and self.thread.is_alive():
            self._notify("브라우저가 이미 실행 중입니다.")
            return
        
        self.driver_ready.clear()
        self.making_driver.set()

        self.stop_event.clear()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        try:
            self._make_driver()
            self.driver_ready.set()        # ✅ 생성 완료 신호
            self._notify("브라우저가 준비되었습니다.")
        except Exception as e:
            self._notify(f"드라이버 생성 실패: {e}")
            return

        while not self.stop_event.is_set():
            try:
                task = self.cmd_q.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                self.cancel_event.clear()
                task()
            except Exception as e:
                self._notify(f"작업 에러: {e}")

        try:
            self.driver.quit()
        except Exception:
            pass
        self.driver = None
        self._notify("브라우저가 종료되었습니다.")


    # 시작 부분!! 밴드 로그인 바로 해버리기!!!
    def _make_driver(self):
        
        nowPath = os.getcwd()
        print(nowPath)
        pg.alert('프로그램을 시작합니다.')

        opts = Options()
        if self.headless:
            opts.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=opts)
        self.driver.set_page_load_timeout(60)

        self.driver.get('https://band.us')
        wait_ready(self.driver)

        while True:
            wait_float(1.5, 2.5)
            try:
                loginBtn = self.driver.find_element(by=By.CSS_SELECTOR, value="._loginBtn")
                loginBtn.click()
                break
            except Exception as e:
                print(e)
                pass
        while True:
            wait_float(1.5, 2.5)
            try:
                naverLoginBtn = self.driver.find_element(by=By.CSS_SELECTOR, value=".-naver.externalLogin")
                naverLoginBtn.click()
                break
            except Exception as e:
                print(e)
                pass

        try:
            with open(f'./etc/idpwd.txt', 'rt', encoding='UTF8') as f:
                idpwd = f.read()
        except:
            pass

        try:
            with open(f'./etc/idpwd.txt', 'r') as f:
                idpwd = f.read()
        except:
            pass

        if idpwd == '':
            pg.alert('아이디 비번 파일이 비어 있습니다. 확인 부탁해주세요!')
            self.driver.quit()
            self.cancel_event.set()
            self.stop_event.set()
            if self.thread:
                self.thread.join(timeout=3)
            self.busy.clear()
            self.scroll_pending = False

        getId = idpwd.split(',')[0]
        getpwd = idpwd.split(',')[1]

        print(getId)
        print(getpwd)

        while True:
            focus_window('Chrome')
            wait_float(1.5, 2.5)
            try:
                idInput = self.driver.find_element(by=By.CSS_SELECTOR, value="#id")

                cb.copy(getId)
                wait_float(0.5,1.2)
                idInput.click()
                wait_float(0.5,1.2)
                pg.hotkey('ctrl', 'v')
                wait_float(0.5, 1.2)
            except:
                continue
            try:
                pwdInput = self.driver.find_element(by=By.CSS_SELECTOR, value="#pw")

                cb.copy(getpwd)
                wait_float(0.5,1.2)
                pwdInput.click()
                wait_float(0.5,1.2)
                pg.hotkey('ctrl', 'v')
                wait_float(0.5, 1.2)
            except:
                pass

            try:
                loginSuccessBtnActiveChk = self.driver.find_elements(by=By.CSS_SELECTOR, value=".btn_login.next_step.nlog-click.off")
                if len(loginSuccessBtnActiveChk) == 0:
                    loginSuccessBtnActive = self.driver.find_element(by=By.CSS_SELECTOR, value=".btn_login.next_step.nlog-click")
                    loginSuccessBtnActive.click()
                    break
            except:
                pass

        while True:
            try:
                wait_float(1.5,.25)
                bandMainChk = self.driver.find_elements(by=By.CSS_SELECTOR, value=".headerWidgetArea")
                if len(bandMainChk) > 0:
                    break
            except Exception as e:
                print('메인페이지 못찾는 에러!!')



    

    def stop(self):
        self.cancel_event.set()
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=3)
        self.busy.clear()
        self.scroll_pending = False

    def cancel_current_task(self):
        self.cancel_event.set()
        self._notify("진행 중인 작업에 취소 신호를 보냈습니다.")

    
    def start_band_join(self):
        """
        네이버 스크롤은 '길게 도는 작업'이므로
        - 실행 중(busy) 이거나
        - 대기 중(scroll_pending) 이면
        새로 요청된 스크롤은 '무시'하고 메시지만 띄웁니다.
        """

        if not self.driver_ready.is_set():   # 또는: if self.driver is None:
            self._alert_not_ready()
            return
        

        if self.busy.is_set() or self.join_pending:
            self._notify("작업중입니다. 먼저 멈춤을 눌러주세요.")
            return

        # 여기서부터 '대기 중'으로 표시 (큐에 넣기 직전)
        self.join_pending = True

        def job():
            # 워커 스레드에서 한 번 더 안전 체크 (레이스 방지)
            if self.stop_event.is_set():
                self.join_pending = False
                return
            if self.busy.is_set():
                self._notify("이미 다른 작업이 실행 중입니다.")
                self.join_pending = False
                return

            self.busy.set()  # 길게 도는 작업 시작!
            self.join_pending = False
            self._notify("밴드 가입 작업을 시작합니다. (멈춤 버튼으로 중단 가능)")

            try:
                band_join_loop(
                    self.driver,
                    self.cancel_event,
                    self.stop_event,
                )
            finally:
                self.busy.clear()
                self._notify("밴드 가입 작업이 종료되었습니다.")

        self.cmd_q.put(job)

    def start_band_write(self):
        """
        네이버 스크롤은 '길게 도는 작업'이므로
        - 실행 중(busy) 이거나
        - 대기 중(scroll_pending) 이면
        새로 요청된 스크롤은 '무시'하고 메시지만 띄웁니다.
        """

        if not self.driver_ready.is_set():   # 또는: if self.driver is None:
            self._alert_not_ready()
            return
        

        if self.busy.is_set() or self.scroll_pending:
            self._notify("작업중입니다. 먼저 멈춤을 눌러주세요.")
            return

        # 여기서부터 '대기 중'으로 표시 (큐에 넣기 직전)
        self.scroll_pending = True

        def job():
            # 워커 스레드에서 한 번 더 안전 체크 (레이스 방지)
            if self.stop_event.is_set():
                self.scroll_pending = False
                return
            if self.busy.is_set():
                self._notify("이미 다른 작업이 실행 중입니다.")
                self.scroll_pending = False
                return

            self.busy.set()  # 길게 도는 작업 시작!
            self.scroll_pending = False
            self._notify("밴드 글쓰기 작업을 시작합니다. (멈춤 버튼으로 중단 가능)")

            try:
                band_write_loop(
                    self.driver,
                    self.cancel_event,
                    self.stop_event,
                )
            finally:
                self.busy.clear()
                self._notify("밴드 가입 작업이 종료되었습니다.")

        self.cmd_q.put(job)

    # 선택: 대기 중 작업 비우기
    def clear_pending(self):
        cleared = 0
        try:
            while True:
                self.cmd_q.get_nowait()
                self.cmd_q.task_done()
                cleared += 1
        except queue.Empty:
            pass
        if cleared:
            self._notify(f"대기 중 작업 {cleared}개를 비웠습니다.")

    def _alert_not_ready(self):
        # 우선 pyautogui.alert (pg.alert) 시도, 안 되면 Tk messagebox로 폴백
        try:
            pg.alert("밴드 로그인이 완료되지 않았습니다. 밴드 로그인을 먼저 완료 해주세요", "알림")
        except Exception:
            try:
                from tkinter import messagebox
                messagebox.showwarning("알림", "브라우저 준비 중입니다.\n초기화가 끝난 뒤 다시 시도하세요.")
            except Exception:
                # 마지막 폴백: 콘솔
                print("[알림] 브라우저 준비 중입니다. 초기화가 끝난 뒤 다시 시도하세요.")