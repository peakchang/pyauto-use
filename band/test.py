import threading, queue, time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BrowserWorker:
    def __init__(self):
        self.cmd_q = queue.Queue()
        self.stop_event = threading.Event()    # 전체 종료 시그널
        self.cancel_event = threading.Event()  # 현재 작업만 취소
        self.thread = None
        self.driver = None

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        try:
            opts = Options()
            # opts.add_argument('--headless=new')  # 필요시
            self.driver = webdriver.Chrome(options=opts)
            self.driver.set_page_load_timeout(60)
        except Exception as e:
            print("드라이버 생성 실패:", e); return

        while not self.stop_event.is_set():
            try:
                task = self.cmd_q.get(timeout=0.1)
            except queue.Empty:
                continue
            try:
                self.cancel_event.clear()  # 새 작업 시작 전 리셋
                task()
            except Exception as e:
                print("작업 에러:", e)

        try: self.driver.quit()
        except: pass
        self.driver = None

    def _wait_ready(self, timeout=15):
        end = time.time() + timeout
        while time.time() < end:
            try:
                if self.driver.execute_script("return document.readyState") == "complete":
                    return True
            except: pass
            time.sleep(0.1)
        return False

    # 네이버에서 무한 스크롤 (끝까지 내려가면 맨 위로 올라가 반복)
    def start_naver_scroll(self, url="https://news.naver.com/", step=800, interval=0.3,
                           max_idle_rounds=8, loop_top=True):
        def job():
            d = self.driver
            d.get(url)
            self._wait_ready()

            idle = 0
            while not self.cancel_event.is_set() and not self.stop_event.is_set():
                try:
                    last_h = d.execute_script(
                        "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
                    d.execute_script(f"window.scrollBy(0, {int(step)});")
                    time.sleep(interval)
                    new_h = d.execute_script(
                        "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
                    y = d.execute_script("return window.pageYOffset || document.documentElement.scrollTop")

                    # 바닥 근접 + 높이 증가 없음 체크
                    if new_h <= last_h and y + 1000 >= new_h:
                        idle += 1
                    else:
                        idle = 0

                    if idle >= max_idle_rounds:
                        if loop_top:
                            d.execute_script("window.scrollTo(0, 0);")
                            time.sleep(0.5)
                            idle = 0
                        else:
                            time.sleep(interval)
                except Exception as e:
                    print("스크롤 중 오류:", e)
                    break
        self.cmd_q.put(job)

    def cancel_current_task(self):
        self.cancel_event.set()  # 현재 진행 중 작업만 중단

    def stop(self):
        self.cancel_event.set()
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=3)

# ===== Tkinter UI =====
root = tk.Tk()
root.title("네이버 스크롤 데모")
root.geometry("360x210")

worker = BrowserWorker()

tk.Button(root, text="브라우저 시작", width=26, command=worker.start).pack(pady=6)

tk.Button(root, text="네이버 무한 스크롤 시작", width=26,
          command=lambda: worker.start_naver_scroll("https://news.naver.com/")).pack(pady=6)

tk.Button(root, text="스크롤 멈추기(작업 취소)", width=26,
          command=worker.cancel_current_task).pack(pady=6)
tk.Button(root, text="브라우저 닫기", width=26, command=worker.stop).pack(pady=6)

def on_close():
    worker.stop()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
