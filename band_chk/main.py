# main.py
import tkinter as tk
from tkinter import ttk
from action import BrowserWorker

def main():
    root = tk.Tk()
    root.title("Selenium 제어 UI")
    root.geometry("460x280")
    root.resizable(False, False)

    # 메시지를 UI 스레드에서 안전하게 표시하는 콜백
    status_var = tk.StringVar(value="대기 중")
    def notifier(msg: str):
        root.after(0, lambda: status_var.set(msg))

    worker = BrowserWorker(headless=False, on_message=notifier)

    frame = ttk.LabelFrame(root, text="브라우저 제어")
    frame.pack(fill="both", expand=True, padx=10, pady=10)





    # 버튼들
    ttk.Button(frame, text="브라우저 시작", width=24, command=worker.start)\
        .grid(row=2, column=0, padx=6, pady=6, sticky="w")
    
    ttk.Button(frame, text="밴드 가입 시작", width=24,
               command=lambda: worker.start_band_join())\
        .grid(row=2, column=1, padx=6, pady=6, sticky="w")

    ttk.Button(frame, text="네이버 스크롤 시작", width=24,
               command=lambda: worker.start_band_write(
                   step=900, interval=0.25,
                   loop_top=True, max_idle_rounds=6
               ))\
        .grid(row=3, column=0, padx=6, pady=6, sticky="w")
    

    ttk.Button(frame, text="스크롤 멈추기(현재 작업만)", width=24,
               command=worker.cancel_current_task)\
        .grid(row=3, column=1, padx=6, pady=6, sticky="w")

    ttk.Button(frame, text="브라우저 닫기(전체 종료)", width=24,
               command=worker.stop)\
        .grid(row=4, column=0, padx=6, pady=6, sticky="w")
    ttk.Button(frame, text="대기 작업 비우기", width=24,
               command=worker.clear_pending)\
        .grid(row=4, column=1, padx=6, pady=6, sticky="w")

    # 상태 라벨
    ttk.Separator(root).pack(fill="x", padx=10, pady=(0,6))
    ttk.Label(root, textvariable=status_var, anchor="w").pack(fill="x", padx=14, pady=(0,10))

    def on_close():
        worker.stop()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    main()
