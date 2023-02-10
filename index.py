import tkinter
import time
import face_recognition
import customtkinter
import cv2
from PIL import Image, ImageTk
import os, sys
import numpy as np
import math

known_face_encodings = []
known_face_names = []
# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


def encode_faces():
    for image in os.listdir('faces'):
        face_image = face_recognition.load_image_file(f"faces/{image}")
        print(face_recognition.face_encodings(face_image))
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(image)
        print(known_face_names)

# init all face data before starting the app
encode_faces()

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create Tk window
app.geometry("800x600")
app.title("Face Recognition")

webcam = cv2.VideoCapture(0)



def update_frame(label):
    _, frame = webcam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    height, width, _ = frame.shape
    center_x, center_y = int(width / 2), int(height / 2)
    radius = int(min(width, height) / 4)
    color = (119,136,153)
    epaisseur = 2

    cv2.circle(frame, (center_x, center_y), radius, color, epaisseur, cv2.LINE_AA)
    frame = customtkinter.CTkImage(Image.fromarray(frame), size=(400, 400))
    label.configure(image=frame)

    label.after(5, lambda: update_frame(label))

def run_recognition(label):

    if not webcam.isOpened():
        sys.exit('Video source not found...')

    ret, frame = webcam.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Inconnu"
        # confidence = '???'
        # Calculate the shortest distance to face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            name = os.path.splitext(name)[0]            # confidence = face_confidence(face_distances[best_match_index])
        face_names.append(f'{name}')
            # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
            # Check the name and choose the color accordingly
        if name == "Inconnu":
            color = (0, 0, 255) # Red
        else:
            color = (0, 255, 0) # Green

        # Create the frame with the name
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = customtkinter.CTkImage(Image.fromarray(frame), size=(400, 400))
    label.configure(image=frame)
    label.after(10, lambda: run_recognition(label))

def home_page(): 
    home_frame = customtkinter.CTkFrame(master=main_frame)
    home_frame.pack(pady=10, padx=10)

    label = customtkinter.CTkLabel(master=home_frame, text="BIENVENUE SUR VOTRE SYSTEM DE SÉCURITÉ \n DE RECONNAISSANCE FACIALE", font=("Arial", 20))
    label.pack(pady=10, padx=10)

    enter = customtkinter.CTkEntry(master=home_frame, placeholder_text="Enter your username")
    enter.pack(pady=10, padx=10)

    button = customtkinter.CTkButton(master=home_frame, text="TakePhoto")
    button.pack(pady=10, padx=10)

def register_page(): 

    global buttonPicture
    global labelCamera
    global buttonPicture
    global home_frame


    home_frame = customtkinter.CTkFrame(master=main_frame, fg_color="white")
    home_frame.pack(pady=10, padx=10)

    label = customtkinter.CTkLabel(master=home_frame, text="Enregistrer \n une nouvelle personne", font=("Arial", 20))
    label.pack(pady=10, padx=10)

    labelCamera = customtkinter.CTkLabel(master=home_frame, text="")
    labelCamera.pack(pady=10, padx=10)

    enter = customtkinter.CTkEntry(master=home_frame, placeholder_text="Entrez votre nom")
    enter.pack(pady=10, padx=10)

    buttonPicture = customtkinter.CTkButton(master=home_frame, text="S'enregistrer", command=lambda: takePicture(enter))
    buttonPicture.pack(pady=10, padx=10)

    update_frame(labelCamera)

def scan_page(): 
    home_frame = customtkinter.CTkFrame(master=main_frame)
    home_frame.pack(pady=10, padx=10)

    label = customtkinter.CTkLabel(master=home_frame, text="    START SCANNING", font=("Arial", 20))
    label.pack(pady=10, padx=10)

    labelCamera = customtkinter.CTkLabel(master=home_frame, text="")
    labelCamera.pack(pady=10, padx=10)

    enter = customtkinter.CTkEntry(master=home_frame, placeholder_text="Enter your username")
    enter.pack(pady=10, padx=10)

    run_recognition(labelCamera)

def hideIndicator():
    home_button_is_active.configure(fg_color="transparent")
    register_button_is_active.configure(fg_color="transparent")
    start_scan_button_is_active.configure(fg_color="transparent")

def refresh_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def isActive(button, page):
    hideIndicator()
    button.configure(fg_color="blue")
    refresh_frame()
    page()

def takePicture(enter):
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
            encode_faces()
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

        #home_frame.after(1000, lambda: home_frame.configure(fg_color="black"))


# adding navigation menu
leftSideMenu = customtkinter.CTkFrame(master=app)
leftSideMenu.configure(width=200)
leftSideMenu.pack(side="left", fill="y", pady=0)

home_button = customtkinter.CTkButton(master=leftSideMenu, text="Accueil", fg_color="blue", command=lambda:isActive(home_button_is_active, home_page))
home_button.pack(pady=10, padx=50)

home_button_is_active = customtkinter.CTkLabel(master=leftSideMenu, width=1, height=40, fg_color="transparent", text=" ")
home_button_is_active.place(x=0, y=5)


register_button = customtkinter.CTkButton(master=leftSideMenu, text="S'enregister",fg_color="blue", command=lambda:isActive(register_button_is_active, register_page))
register_button.pack(pady=10, padx=50)

register_button_is_active = customtkinter.CTkLabel(master=leftSideMenu, width=1, height=40, fg_color="transparent", text=" ")
register_button_is_active.place(x=0, y=50)


start_scan_button = customtkinter.CTkButton(master=leftSideMenu, text="Commencer un scan",fg_color="blue", command=lambda:isActive(start_scan_button_is_active, scan_page))
start_scan_button.pack(pady=10, padx=50)

start_scan_button_is_active = customtkinter.CTkLabel(master=leftSideMenu, width=1, height=40, fg_color="transparent", text=" ")
start_scan_button_is_active.place(x=0, y=100)

# adding main frame 
main_frame = customtkinter.CTkFrame(master=app, fg_color="blue")
main_frame.pack(side="right", fill="both", expand=True, pady=0)

app.mainloop()