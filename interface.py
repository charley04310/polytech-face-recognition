import customtkinter
import cv2
from PIL import Image, ImageTk
from recognition import WebCamMethods

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class Interface:
    def __init__(self):

        self.isAuth = False
        self.recognition = WebCamMethods()

        self.master = customtkinter.CTk() 
        self.master.title("Face Recognition System")
        self.master.geometry("800x600")

        self.webcam = cv2.VideoCapture(0)

        self.leftSideMenu()
        
        self.main_frame = customtkinter.CTkFrame(master=self.master, fg_color="blue")
        self.main_frame.pack(side="right", fill="both", expand=True, pady=0)

        self.router_recognition(self.home_button_is_active, self.home_page)

        self.master.mainloop()

    def update_frame(self, label):
        _, frame = self.webcam.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        height, width, _ = frame.shape
        center_x, center_y = int(width / 2), int(height / 2)
        radius = int(min(width, height) / 4)
        color = (119,136,153)
        epaisseur = 2

        cv2.circle(frame, (center_x, center_y), radius, color, epaisseur, cv2.LINE_AA)
        frame = customtkinter.CTkImage(Image.fromarray(frame), size=(400, 400))
        label.configure(image=frame)

        label.after(5, lambda: self.update_frame(label))

    def leftSideMenu(self):
            self.leftSideMenu = customtkinter.CTkFrame(master=self.master)
            self.leftSideMenu.configure(width=200)
            self.leftSideMenu.pack(side="left", fill="y", expand=False, pady=0)

            self.home_button = customtkinter.CTkButton(master=self.leftSideMenu, text="Accueil", fg_color="blue", command=lambda:self.router_recognition(self.home_button, self.home_page))
            self.home_button.pack(pady=10, padx=50)

            self.home_button_is_active = customtkinter.CTkLabel(master=self.leftSideMenu, width=2, height=40, fg_color="transparent", text=" ")
            self.home_button_is_active.place(x=0, y=0)
            self.register_button = customtkinter.CTkButton(master=self.leftSideMenu, text="S'enregister",fg_color="blue", command=lambda:self.router_recognition(self.register_button_is_active, self.register_page))
            self.register_button.pack(pady=10, padx=50)

            self.register_button_is_active = customtkinter.CTkLabel(master=self.leftSideMenu, width=2, height=40, fg_color="transparent", text=" ")
            self.register_button_is_active.place(x=0, y=50)

            self.start_scan_button = customtkinter.CTkButton(master=self.leftSideMenu, text="Commencer un scan",fg_color="blue", command=lambda:self.router_recognition(self.start_scan_button_is_active, self.scan_page))
            self.start_scan_button.pack(pady=10, padx=50)

            self.start_scan_button_is_active = customtkinter.CTkLabel(master=self.leftSideMenu, width=2, height=40, fg_color="transparent", text=" ")
            self.start_scan_button_is_active.place(x=0, y=100)

    def home_page(self): 
        self.home_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.home_frame.pack(pady=10, padx=10)

        self.image_introduction = customtkinter.CTkImage(Image.open("img/face.jpeg"), size=(600, 400))

        self.label = customtkinter.CTkLabel(master=self.home_frame, text="BIENVENUE SUR VOTRE SYSTEM DE SÉCURITÉ \n DE RECONNAISSANCE FACIALE", font=("Arial", 20))
        self.label.pack(pady=10, padx=10)

        self.label_image = customtkinter.CTkLabel(master=self.home_frame, text="")
        self.label_image.pack(pady=10, padx=10)
        self.label_image.configure(image=self.image_introduction)

        if self.isAuth == True:
            self.button = customtkinter.CTkButton(master=self.home_frame, text="Se déconnecter", command=self.log_out())
            self.button.pack(pady=10, padx=10)

        else:
            self.enter = customtkinter.CTkEntry(master=self.home_frame, placeholder_text="code d'identification")
            self.enter.pack(pady=10, padx=10)

            self.button = customtkinter.CTkButton(master=self.home_frame, text="Votre code d'identification", command=lambda:self.isCodeValidate(self.enter))
            self.button.pack(pady=10, padx=10)

    def register_page(self): 

        self.home_frame = customtkinter.CTkFrame(master=self.main_frame, fg_color="white")
        self.home_frame.pack(pady=10, padx=10)

        self.label = customtkinter.CTkLabel(master=self.home_frame, text="Enregistrer \n une nouvelle personne", font=("Arial", 20))
        self.label.pack(pady=10, padx=10)

        self.labelCamera = customtkinter.CTkLabel(master=self.home_frame, text="")
        self.labelCamera.pack(pady=10, padx=10)

        self.enter = customtkinter.CTkEntry(master=self.home_frame, placeholder_text="Entrez votre nom")
        self.enter.pack(pady=10, padx=10)

        self.buttonPicture = customtkinter.CTkButton(master=self.home_frame, text="S'enregistrer", command=lambda:self.recognition.takePicture(self.webcam, self.labelCamera, self.enter, self.buttonPicture, self.home_frame))
        self.buttonPicture.pack(pady=10, padx=10)

        self.update_frame(self.labelCamera)

    def scan_page(self): 
        self.home_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.home_frame.pack(pady=10, padx=10)

        self.label = customtkinter.CTkLabel(master=self.home_frame, text="    START SCANNING", font=("Arial", 20))
        self.label.pack(pady=10, padx=10)

        self.labelCamera = customtkinter.CTkLabel(master=self.home_frame, text="")
        self.labelCamera.pack(pady=10, padx=10)

        self.recognition.run_recognition(self.webcam, self.labelCamera)
    
    def hideIndicator(self):
        self.home_button_is_active.configure(fg_color="transparent")
        self.register_button_is_active.configure(fg_color="transparent")
        self.start_scan_button_is_active.configure(fg_color="transparent")

    def refresh_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def router_recognition(self, button, page):
        self.hideIndicator()
        button.configure(fg_color="blue")
        self.refresh_frame()
        page()
    
    def isCodeValidate(self, enter):
        if enter.get() == "1234":
            self.isAuth = True
            print("isAuth == true ")

        else:
            print("isAuth == flase")
    
    def log_out(self):
        self.isAuth = False
        self.router_recognition(self.home_button_is_active, self.home_page)