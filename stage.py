import tkinter as tk 
from PIL import Image, ImageTk
import cv2
import numpy as np
from timer import Timer
#import score


class Stage(tk.Frame):
    def __init__(self, master, timer):
        super().__init__(master)
        self.master = master

        # timer
        self.timer = timer

        # 成功したフレームの数
        self.success_counter = 0

        # クリアに必要な成功フレームの回数
        self.required_frame = 10
        
        #score
        self.score = 0
        self.scoredis = tk.Label(master, height=5, width=10, textvariable="")
        self.scoredis.config(text="Score: 0")
        self.scoredis.grid(row=1, column=3, columnspan=1)

        #stage
        self.stage = 0
        self.stagedis = tk.Label(master, height=5, width=10, textvariable="")
        self.stagedis.config(text="STAGE %d" % (self.stage + 1))
        self.stagedis.grid(row=2, column=3, columnspan=1)
        
        #image
        self.image_num = 5
        img_1 = ImageTk.PhotoImage(Image.open("img_save1.png").resize((400, 300), Image.NEAREST))
        img_2 = ImageTk.PhotoImage(Image.open("img_save2.png").resize((400, 300), Image.NEAREST))
        img_3 = ImageTk.PhotoImage(Image.open("img_save3.png").resize((400, 300), Image.NEAREST))
        img_4 = ImageTk.PhotoImage(Image.open("img_save4.png").resize((400, 300), Image.NEAREST))
        img_5 = ImageTk.PhotoImage(Image.open("img_save5.png").resize((400, 300), Image.NEAREST))
        self.image_list = [img_1,img_2,img_3,img_4,img_5]
        self.my_label = tk.Label(image = self.image_list[0])
        self.my_label.grid(row=1, column=2, columnspan=1)
        self.start_button = tk.Button(master,text="next", width=8, height=4, command=lambda:self.nextStage())
        self.start_button.grid(row=3, column=3, columnspan=1)

        #button
        self.start_button = tk.Button(master, bg="Green", text="Start", width=8, height=4, command=self.timer.start)
        self.start_button.grid(row=1, column=0)

        self.pause_button = tk.Button(master, bg="Red", text="Restart", width=8, height=4, command=self.restart)
        self.pause_button.grid(row=1, column=1)

    # 一定フレーム以上クリアしたら次のステージへ(メインから呼ぶ関数)
    def success(self):
        self.success_counter += 1
        if (self.success_counter > self.required_frame):
            self.success_counter = 0
            self.nextStage()
            self.timer.cleared()

    # 初めから
    def restart(self):
        self.success_counter = 0
        self.score = -100
        self.stage = -1
        self.nextStage()
        self.timer.restart()

    # 次のステージへ
    def nextStage(self):
        self.score += 100
        self.stage += 1
        print("stage: %d" % self.stage)

        # 用意された画像枚数をステージ数が超えたらループ
        if self.stage == self.image_num:
            self.stage = 0
        
        self.scoredis.config(text="Score: %d" % self.score)
        self.stagedis.config(text="STAGE %d" % (self.stage + 1))
        
        self.my_label.grid_forget()
        self.my_label = tk.Label(image = self.image_list[self.stage])
        self.my_label.grid(row=1, column=2, columnspan=1)
        

if __name__ == '__main__':
    root = tk.Tk()
    cd = Stage(root)
    cd.mainloop()
        