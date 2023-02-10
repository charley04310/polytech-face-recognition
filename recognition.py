import time
import face_recognition
import customtkinter
import cv2
from PIL import Image, ImageTk
import os, sys
import numpy as np
import math

class WebCamMethods:

    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.encode_faces()

    def face_confidence(self, face_distance, face_match_threshold=0.6):
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)

        if face_distance > face_match_threshold:
            return str(round(linear_val * 100, 2)) + '%'
        else:
            value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

    def run_recognition(self, webcam, label):
        if not webcam.isOpened():
            sys.exit('Video source not found...')

        ret, frame = webcam.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Inconnu"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                name = os.path.splitext(name)[0]
            face_names.append(f'{name}')

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            if name == "Inconnu":
                color = (0, 0, 255) # Red
            else:
                color = (0, 255, 0) # Green

            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = customtkinter.CTkImage(Image.fromarray(frame), size=(400, 400))
        label.configure(image=frame)
        label.after(10, lambda: self.run_recognition(webcam, label))

    def takePicture(self, webcam, labelCamera, enter, buttonPicture, home_frame):
        name = enter.get()
        path = 'faces/'+name+'.jpg'
        _, main_frame = webcam.read()


        if len(name) == 0:
            labelCamera.configure(text="Veuillez entrer un nom !", font=("Arial", 20), text_color=("white"))
            labelCamera.update()
            time.sleep(1)
            labelCamera.configure(text="", font=("Arial", 20))
            labelCamera.update()

        else:
            labelCamera.configure(text=f"Ne bougez plus et fixer la caméra !", font=("Arial", 20), text_color=("white"))
            labelCamera.update()
            time.sleep(1)

            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(main_frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            if len(faces) == 0:
                labelCamera.configure(text="Aucun visage détecté. \n Veuillez mettre votre visage dans l'oval.")
                labelCamera.update()
                time.sleep(1)
                labelCamera.configure(text="")
                labelCamera.update()

            else:

                for i in range(3, 0, -1):
                    labelCamera.configure(text=f"Taking picture in {i}...", font=("Arial", 20))
                    labelCamera.update()
                    time.sleep(1)

                cv2.imwrite(filename=path, img=main_frame)
                enter.delete(0, 'end')
                self.encode_faces()
                labelCamera.configure(text="Picture taken!")
                labelCamera.update()
                buttonPicture.configure(state="disabled")
                buttonPicture.update()
                home_frame.configure(fg_color="green")
                home_frame.update()

                time.sleep(1)
                buttonPicture.configure(state="normal")
                buttonPicture.update()
                home_frame.configure(fg_color="white")
                home_frame.update()
                labelCamera.configure(text="")
