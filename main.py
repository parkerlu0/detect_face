# -*- coding: utf-8 -*-

#準備
#python3.7環境で確認
#conda install -c conda-forge opencv
#conda install -c conda-forge dlib
#conda install -c conda-forge imutils

import os
import cv2
import dlib
import numpy as np
from imutils import face_utils

import tkinter as tk 
from PIL import Image, ImageTk

from timer import Timer
from stage import Stage
#from timer import Picture

def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result

class Game(tk.Frame):

    #コンストラクタ
    def __init__(self, st, timer, master=None):
        super().__init__(master)

        # stage
        self.st = st

        # timer
        self.timer = timer

        # 閾値（どれだけ正しければよいか）設定、小さいほど難しい
        self.threshold = 0.35

        # 自身(tkinter.Frame)をmaster（mainで作ったroot）に配置
        self.master = master
        
        # MainPanel を 全体に配置
        self.mainpanel = tk.Label(root)
        self.mainpanel.grid(row=3, column=2, columnspan=1)

        # open web cam stream (複数webcamがある場合は，引数を変更する)
        self.cap   = cv2.VideoCapture(0)
        ret, frame = self.cap.read()
        if ret == 0 :
            print("failed to webcam")
            exit()

        # 識別器の準備        
        self.detector = dlib.get_frontal_face_detector()
        predictor_path = 'shape_predictor_68_face_landmarks.dat'
        self.face_predictor = dlib.shape_predictor(predictor_path)

        # 正解画像データのロード
        self.correct_data = [np.loadtxt('img_1.txt'),
                             np.loadtxt('img_2.txt'),
                             np.loadtxt('img_3.txt'),
                             np.loadtxt('img_4.txt'),
                             np.loadtxt('img_5.txt')]

    # ビデオ更新
    def update_video(self):
        ret, frame = self.cap.read()

        self.master.geometry('800x800')
        frame = cv2.resize(frame, (400,300), interpolation=cv2.INTER_LANCZOS4)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #顔検出
        dets, score, idx = self.detector.run(frame, 0)
        for r in dets:
            # 顔ランドマーク検出
            landmark = self.face_predictor(frame, r)
            landmark = face_utils.shape_to_np(landmark)

            # ランドマーク番号描画
            for (i, (x, y)) in enumerate(landmark):
                cv2.circle(frame, (x, y), 2, (255, 128, 0), -1)
            #    cv2.putText(frame, str(i), (x-3, y-3), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))

            # データの正規化
            data = min_max(np.asarray(landmark), 0)

            # 正解データベクトルとのユークリッド距離を計算
            diff = np.linalg.norm(data - self.correct_data[self.st.stage])

            # データ判定
            if diff <= self.threshold:
                print('OK(' + str(diff) + ')')
                cv2.putText(frame, 'correct(' + str(diff) + ')', (20, 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255))
                frame = cv2.rectangle(frame,(r.left(), r.top()), (r.right(), r.bottom()), (0,255,0), 2)
                if self.timer.state == True:
                    self.st.success()
            else:
                print('NG(' + str(diff) + ')')
                cv2.putText(frame, 'incorrect!(' + str(diff) + ')', (20, 20), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255))
                frame = cv2.rectangle(frame,(r.left(), r.top()), (r.right(), r.bottom()), (255,0,0), 2)

        # メインパネルへと描画
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(frame))
        self.mainpanel.imgtk = imgtk
        self.mainpanel.configure(image=imgtk)

        # 33ms後に自分自身を呼ぶ(30fps)
        self.mainpanel.after(33, self.update_video)
    
        
if __name__ == '__main__':
    root = tk.Tk()
    my_timer = Timer(root)
    cd = Stage(root, timer=my_timer)
    game = Game(master=root, st=cd, timer=my_timer)
    game.update_video()
    root.mainloop()
    
