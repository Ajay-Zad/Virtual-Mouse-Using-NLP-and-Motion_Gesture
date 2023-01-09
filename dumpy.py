import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import pyaudio
import sys
import pywhatkit
import datetime
import wikipedia
import pyjokes
from geopy import distance
from geopy.geocoders import Nominatim
import requests
import folium

ans = int(input("enter 0  for head and 1 for hand: "))
if ans == 0:
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame,1)
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape 
        cnt = 0
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id,landmark in enumerate(landmarks[0:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame,(x,y),3,(0,255,0))
                if id == 1:
                    screen_x = int(landmark.x * screen_w)
                    screen_y = int(landmark.y * screen_h)
                    pyautogui.moveTo(screen_x,screen_y)
                    print(screen_x,screen_y)
        cv2.imshow("Eye controlled mouse",frame)
        cv2.waitKey(1)
        
        listener = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("listing")       
                voice = listener.listen(source,0.40,1)
                command = listener.recognize_google(voice)
                print(command)
        except:
            pass
else:
    cap = cv2.VideoCapture(0)
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_w, screen_h = pyautogui.size()
    index_y = 0
    while True:
        _,frame = cap.read()
        frame = cv2.flip(frame,1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame,hand)
                landmarks = hand.landmark
                for id,landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == 8:
                        cv2.circle(img=frame,center=(x,y), radius=10, color=(0,255,255))
                        index_x = screen_w/frame_width * x
                        index_y = screen_h/frame_height * y
                        pyautogui.moveTo(index_x,index_y)
                    if id == 4:
                        cv2.circle(img=frame,center=(x,y), radius=10, color=(255,255,255))
                        thumb_x = screen_w/frame_width * x
                        thumb_y = screen_h/frame_height * y
                        print(abs(index_y - thumb_y))
                        if abs(index_y - thumb_y) < 30:
                            print("click")
                            pyautogui.click()
                            
        cv2.imshow('Virtual_Hand_Mouse',frame)
        cv2.waitKey(1)
        
      
        
    



    
    