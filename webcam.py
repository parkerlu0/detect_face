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

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)

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
            cv2.putText(frame, str(i), (x-3, y-3), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 255, 255))

    cv2.imshow('dlg', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()