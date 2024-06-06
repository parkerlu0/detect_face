import os
import cv2
import dlib
import tkinter as tk 
import numpy as np
from imutils import face_utils

class TakePic(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.button = tk.Button(master, text="Start", width=8, height=4, command=self.take)
        self.button.pack()
    
    def take(self):
        cap = cv2.VideoCapture(0)
        detector = dlib.get_frontal_face_detector()
        predictor_path = 'shape_predictor_68_face_landmarks.dat'
        face_predictor = dlib.shape_predictor(predictor_path)
        ret, frame = cap.read()

        dets, score, idx = detector.run(frame,0)
        for r in dets:
            frame = cv2.rectangle(frame,(r.left(), r.top()), (r.right(), r.bottom()), (255,0,0), 2)

            landmark = face_predictor(frame, r)
            landmark = face_utils.shape_to_np(landmark)
            for (i, (x, y)) in enumerate(landmark):
                cv2.circle(frame, (x, y), 3, (255, 128, 0), -1)

        data = self.min_max(np.asarray(landmark),0)
        cv2.imwrite("img_save1.png", frame)
        np.savetxt('img_1.txt', data)
    
    def min_max(self,x, axis=None):
        min = x.min(axis=axis, keepdims=True)
        max = x.max(axis=axis, keepdims=True)
        result = (x-min)/(max-min)
        return result

root = tk.Tk()
test = TakePic(root)
test.mainloop()
