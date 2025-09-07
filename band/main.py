from ongo import *

def goScriptTraffic():
    getDict = {}
    onth = threading.Thread(target=lambda: bandScript(getDict))
    
    onth.daemon = True
    onth.start()


root = Tk()
root.title("밴드 프로그램")
root.geometry("300x100+500+300")
root.resizable(False, FALSE)


frame0 = LabelFrame(root, text='밴드 프로그램', padx=60, pady=10)  # padx / pady 내부여백
frame0.pack(padx=10, pady=5)  # padx / pady 외부여백


btn1 = Button(frame0, text='시작하기', command=goScriptTraffic, padx=50)
btn1.pack()


# 윈도우창 계속 띄우기
root.mainloop()