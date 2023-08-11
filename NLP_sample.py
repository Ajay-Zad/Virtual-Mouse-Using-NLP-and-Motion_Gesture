import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import threading

# Initialize VideoCapture and FaceMesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# Get screen size
screen_w, screen_h = pyautogui.size()

# Disable pyautogui FAILSAFE (be careful with this)
pyautogui.FAILSAFE = False

# Initialize Speech Recognizer
listener = sr.Recognizer()


def track_head():
    while True:
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process face mesh
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        
        frame_h, frame_w, _ = frame.shape
        
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[0:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                
                if id == 1:
                    screen_x = int(landmark.x * screen_w)
                    screen_y = int(landmark.y * screen_h)
                    pyautogui.moveTo(screen_x, screen_y)
                    
        cv2.imshow("HEAD controlled mouse", frame)
        cv2.waitKey(1)
    
def recognize_speech():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                listener.adjust_for_ambient_noise(source)
                voice = listener.listen(source, timeout=5, phrase_time_limit=1)
                command = str(listener.recognize_google(voice)).lower()
                print(command)
                
                if 'left' in command:
                    print("Left click")
                    pyautogui.click()
                elif 'right' in command:
                    print("Right click")
                    pyautogui.click(button='right')
                elif 'double' in command or 'click' in command:
                    print("Double click")
                    pyautogui.doubleClick()
                elif 'down' in command:
                    print("Scrolling down")
                    pyautogui.scroll(-1500)
                elif 'up' in command or 'scroll' in command or 'sc' in command or 'scr' in command:
                    print("Scrolling up")
                    pyautogui.scroll(1500)
                elif 'start' in command:
                    print("Closing...")
                    pyautogui.click(0, 1079)
                elif 'close' in command:
                    print("Closing...")
                    pyautogui.click(1872, 24)
                elif 'min' in command:
                    print("Minimize")
                    pyautogui.click(1776, -29)
                elif 'add' in command:
                    print("Address bar")
                    pyautogui.click(258, 55)
                    
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Start the head tracking thread
head_thread = threading.Thread(target=track_head)
head_thread.daemon = True
head_thread.start()

# Start the speech recognition thread
speech_thread = threading.Thread(target=recognize_speech)
speech_thread.daemon = True
speech_thread.start()


