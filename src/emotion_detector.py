import cv2
import numpy as np
import os.path
from gtts import gTTS
import os
from cv2 import WINDOW_NORMAL
from face_detection import find_faces

ESC = 27

def start_webcam(model_emotion, window_size, window_name='live', update_time=50):
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    video_feed = cv2.VideoCapture(0)
    video_feed.set(3, width)
    video_feed.set(4, height)
    read_value, webcam_image = video_feed.read()

    delay = 0
    init = True
    while read_value:
        read_value, webcam_image = video_feed.read()
        for normalized_face, (x, y, w, h) in find_faces(webcam_image):
          if init or delay == 0:
            init = False
            emotion_prediction = model_emotion.predict(normalized_face)
            test=emotion_prediction[0]
          cv2.putText(webcam_image, emotions[test], (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
          myobj=gTTS(text=emotions[test],lang='en',slow=False)
          myobj.save("output/text.mp3")
          os.system('mpg321 output/text.mp3')
          
        delay += 1
        delay %= 20
        cv2.imshow(window_name, webcam_image)
        key = cv2.waitKey(update_time)
        if key == ESC:
            break

    cv2.destroyWindow(window_name)

def analyze_picture(model_emotion, path, window_size, window_name='static'):
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    image = cv2.imread(path, 1)
    for normalized_face, (x, y, w, h) in find_faces(image):
        emotion_prediction = model_emotion.predict(normalized_face)
        cv2.putText(image, emotions[emotion_prediction[0]], (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
    cv2.imshow(window_name, image)
    key = cv2.waitKey(0)
    if key == ESC:
        cv2.destroyWindow(window_name)
if __name__ == '__main__':
    emotions = ["afraid", "angry", "disgusted", "happy", "neutral", "sad", "surprised"]

    # Load model
    fisher_face_emotion = cv2.face.FisherFaceRecognizer_create()
    fisher_face_emotion.read('models/emotion_classifier_model.xml')

    

    # Use model to predict
    choice = input("Use webcam?(y/n) ")
    if (choice == 'y'):
        window_name = "Facifier Webcam (press ESC to exit)"
        start_webcam(fisher_face_emotion, window_size=(1280, 720), window_name=window_name, update_time=15)
    elif (choice == 'n'):
        run_loop = True
        window_name = "Facifier Static (press ESC to exit)"
        print("Default path is set to data/sample/")
        print("Type q or quit to end program")
        while run_loop:
            path = "../data/sample/"
            file_name = input("Specify image file: ")
            if file_name == "q" or file_name == "quit":
                run_loop = False
            else:
                path += file_name
                if os.path.isfile(path):
                    analyze_picture(fisher_face_emotion, path, window_size=(1280, 720), window_name=window_name)
                else:
                    print("File not found!")
    else:
        print("Invalid input, exiting program.")

