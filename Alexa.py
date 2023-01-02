# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 19:33:35 2022

@author: Lenovo
"""

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

f = 0
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def AS():
    print("Listining...")
    with sr.Microphone() as source1:
        voice1 = listener.listen(source1)
        command1 = listener.recognize_google(voice1)
        engine.runAndWait()
        return command1    
def comm():
    try:
        if f == 0:
            with sr.Microphone() as source:
                voice = listener.listen(source)
                command = listener.recognize_google(voice)
                engine.say('Hey Hi I am your Alexa')
                engine.say('How can I help you')
                engine.runAndWait()
        
            
        c1 = AS()
        return c1
            
    except:
        pass

def run_AS():
    command = comm()
    if 'play' in command:
        song = command.replace('play','')
        pywhatkit.playonyt(song)
        talk('Playing'+ song)
    elif 'time' in command:
        t = datetime.datetime.now().strftime('%I:%M:%p')
        talk('Current time is '+t)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person,1)
        talk(info)
    elif 'date' in command:
        d = datetime.datetime.today().strftime('%D')
        talk('Today date is '+ d)
    elif 'joke' in command:
        talk("here is a joke for you"+pyjokes.get_joke())
    elif 'what is the distance between' in command:
        command = command.replace('what is the distance between','')
        command = command.split('and')
        geocoder = Nominatim(user_agent='i know python')
        l1 = command[0]
        l2 = command[1]
        c1 = geocoder.geocode(l1)
        c2 = geocoder.geocode(l2)
        ll1,lo1 = c1.latitude,c1.longitude
        ll2,lo2 = c2.latitude,c2.longitude
        p1 = (ll1,lo1)
        p2 = (ll2,lo2)
        talk(distance.distance(p1,p2))
    elif 'what is my current location' in command:
        r = requests.get('https://get.geojs.io/')
        ip_req = requests.get('https://get.geojs.io/v1/ip.json')
        ipAdd = ip_req.json()['ip']
        url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        geo_request = requests.get(url)
        geo_data = geo_request.json()
        print(geo_data)
    else:
        engine.say("okay Thank you See you soon")
        engine.runAndWait() 
        
        
        
        
        
while True:
    run_AS()
    f = f + 1
        
