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

while True:    
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("listing")       
            voice = listener.listen(source)
            print(voice)
            command = listener.recognize_google(voice)
            print(command)
    except:
        pass