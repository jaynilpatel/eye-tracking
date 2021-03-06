śfrom picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BOARD)
 
Motor1A = 16
Motor1B = 18
#Motor1E = 22

Motor2A = 19
Motor2B = 21
#Motor2E = 23

count=0
def moveForwards():
    #print ("Going forwards")

    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)


def stop():
    GPIO.setup(Motor1A,GPIO.OUT)
    GPIO.setup(Motor1B,GPIO.OUT)

    GPIO.setup(Motor2A,GPIO.OUT)
    GPIO.setup(Motor2B,GPIO.OUT)
    #print ("Stopped")
    GPIO.output(Motor1A, GPIO.LOW)
    GPIO.output(Motor2A, GPIO.LOW)
    
RELAY = 17
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyesCascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")

close=0
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = image[y:y + h, x:x + w]
        eyes = eyesCascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (100, 255, 255), 2)

        if len(faces) >= 1 and len(eyes) >= 2:
            print ('close your eyes to start')
        else:
            if(close > 2):
                if count%2==0:
                    print("starting motors")
                    moveForwards()
                    count+=1
                elif count%2!=0:
                    print("Stoping motors")
                    stop()
                    count+=1
                close=-1
            close = close + 1
            time.sleep(1)
            

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    if key == ord("q"):
        break


cv2.destroyAllWindows()
