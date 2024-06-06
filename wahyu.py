# -*- coding: utf-8 -*-
#使い方：
# s = pause/play
# 1~5 = img_1 ~ img_5として保存
# 確認のためは行43のcorrect ファイルを変える



import os
import cv2
import dlib
import numpy as np
from imutils import face_utils

def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)
correct = []
n=0

while 1:
    ret, frame = cap.read()
    
    #顔検出
    dets, score, idx = detector.run(frame,0)
    for r in dets:
        frame = cv2.rectangle(frame,(r.left(), r.top()), (r.right(), r.bottom()), (255,0,0), 2)

        #顔ランドマーク検出
        landmark = face_predictor(frame, r)
        landmark = face_utils.shape_to_np(landmark)
        for (i, (x, y)) in enumerate(landmark):
            cv2.circle(frame, (x, y), 3, (255, 128, 0), -1)
#            cv2.putText(frame, str(i), (x-3, y-3), cv2.FONT_HERSHEY_PLAIN, 0.9, (0, 0, 0))
        data = min_max(np.asarray(landmark),0)
        correct = np.loadtxt('img_3.txt')
#        correct[1] = np.loadtxt('img_1.txt')
#        correct[2] = np.loadtxt('img_2.txt')
#        correct[3] = np.loadtxt('img_3.txt')
#        correct[4] = np.loadtxt('img_4.txt')
#        correct[5] = np.loadtxt('img_5.txt')
        result = np.linalg.norm(data - correct)
        if(result <= 0.3):
            print("correct!!" + str(n))
            n+=1
    cv2.imshow('dlg', frame)
    
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('s'):
#        cv2.imwrite("img_save.png", frame)
#        np.savetxt('test.out', data)
        print(data)
        cv2.waitKey(-1)
        print(r.left())
    elif k == ord('1'):
        cv2.imwrite("img_save1.png", frame)
        np.savetxt('img_1.txt', data)
    elif k == ord('2'):
        cv2.imwrite("img_save2.png", frame)
        np.savetxt('img_2.txt', data)
    elif k == ord('3'):
        cv2.imwrite("img_save3.png", frame)
        np.savetxt('img_3.txt', data)
    elif k == ord('4'):
        cv2.imwrite("img_save4.png", frame)
        np.savetxt('img_4.txt', data)
    elif k == ord('5'):
        cv2.imwrite("img_save5.png", frame)
        np.savetxt('img_5.txt', data)

cap.release()
cv2.destroyAllWindows()
