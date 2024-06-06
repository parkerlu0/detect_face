import tkinter as tk 
from PIL import Image, ImageTk
import cv2
import numpy as np

class Timer:
    def __init__(self,master):
        self.master = master
        master.title("変顔ゲーム")

        # タイマーが動いているかどうか
        self.state = False

        # タイマーが準備状態（ステージが始まる前の準備時間）か
        self.is_ready = True

        # タイマーの初期秒数（リセットしたときの秒数）
        self.init_sec = 10

        # タイマーの現在の秒数
        self.now_sec = 5

        # jobID
        self.jobID = 0

        self.timer = tk.Label(master, height=5, width=10, textvariable="")
        self.timer.config(text="Press Start!!")
        self.timer.grid(row=0, column=0, columnspan=2)


    def countdown(self):
        if self.now_sec == 0:
            if self.is_ready == True:
                self.is_ready = False
                self.now_sec = self.init_sec
                self.timer.config(text="%d" % self.now_sec)
                self.now_sec -= 1
                self.jobID = self.master.after(1000, self.countdown)
            else:
                self.timeout()
        else:
            if self.is_ready == True:
                self.timer.config(text="Ready...(%d)" % self.now_sec)
            else:    
                self.timer.config(text="%d" % self.now_sec)
            self.now_sec -= 1
            self.jobID = self.master.after(1000, self.countdown) 
    
    def start(self):
        if self.state == False:
            self.state = True
            self.is_ready = True
            self.now_sec = self.init_sec / 2
            self.countdown()
    
    def restart(self): 
        self.state = False
        self.is_ready = True
        self.master.after_cancel(self.jobID)
        self.start()

    # クリアしたときの処理
    def cleared(self):
        self.state = False
        self.timer.config(text="Cleared!!")
        self.master.after_cancel(self.jobID)
        self.master.after(1000, self.start)

    # タイマーが0になった時の処理
    def timeout(self):
        self.state = False
        self.timer.config(text="TIME OUT!")

        #if self.state == True:
        #    return 1
        #else:
        #    return 0

class VideoViewer(tk.Frame):

    #コンストラクタ
    def __init__(self, master=None):
        super().__init__(master)

        #自身(tkinter.Frame)をmaster（mainで作ったroot）に配置
        self.master = master
        

        # MainPanel を 全体に配置
        self.mainpanel = tk.Label(root)
        self.mainpanel.grid(row=3, column=2, columnspan=1)

        #open web cam stream (複数webcamがある場合は，引数を変更する)
        self.cap   = cv2.VideoCapture( 0 )
        ret, frame = self.cap.read()
        if ret == 0 :
            print("failed to webcam")
            exit()


    def update_video(self):
        ret, frame = self.cap.read()

        self.master.geometry('800x800')
        frame = cv2.resize(frame, (457,257), interpolation=cv2.INTER_LANCZOS4)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.mainpanel.imgtk = imgtk
        self.mainpanel.configure(image=imgtk)

        #66ms後に自分自身を呼ぶ
        self.mainpanel.after(33, self.update_video)


if __name__ == '__main__':
    root = tk.Tk()
    my_timer = Timer(root)
    #my_pic = Picture(root)
    root.mainloop()

