from tkinter import filedialog
import customtkinter as ctk
import qrcode
import cv2
from PIL import Image
import io


# Hauptklasse für die QR-Code Anwendung
class QRCodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Bildschirmauflösung wird ermittelt
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()

        # App-Maße entsprechen herunterskalierten Screen-Maßen
        app_width = int(SCREEN_WIDTH * 0.5)
        app_height = int(SCREEN_HEIGHT * 0.5)

        self.title("QR-Code Anwendung GSG Schulbibliothek")
        self.geometry(f"{app_width}x{app_height}")
        self.resizable(None, None)
        self.iconbitmap("app_icon_white.ico")

        # Window Grid-Konfiguration
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Frame für QR-Code-Erzeugung
        self.info_frame = ctk.CTkFrame(self, corner_radius=10, border_width=2, border_color="gray")
        self.info_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # "Buchinformationen eingeben" Frame Titel
        self.label_frame_title = ctk.CTkLabel(self.info_frame, text="Buchinformationen eingeben", font=("Arial", 14, "bold"), anchor="w")
        self.label_frame_title.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        # Anordnung der Buchinformationen in einem Grid
        # Erste Zeile: Titel, Autor und Untertitel
        self.entry_titel = ctk.CTkEntry(self.info_frame, placeholder_text="Titel")
        self.entry_titel.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.entry_author = ctk.CTkEntry(self.info_frame, placeholder_text="Autor")
        self.entry_author.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.entry_untertitel = ctk.CTkEntry(self.info_frame, placeholder_text="Untertitel")
        self.entry_untertitel.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        # Zweite Zeile: Verlag, Auflage, Jahr (mittig und verteilt)
        self.entry_verlag = ctk.CTkEntry(self.info_frame, placeholder_text="Verlag")
        self.entry_verlag.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.entry_auflage = ctk.CTkEntry(self.info_frame, placeholder_text="Auflage")
        self.entry_auflage.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.entry_jahr = ctk.CTkEntry(self.info_frame, placeholder_text="Jahr")
        self.entry_jahr.grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        # Dritte Zeile: Kategorie, Anzahl
        self.entry_kategorie = ctk.CTkEntry(self.info_frame, placeholder_text="Kategorie")
        self.entry_kategorie.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.entry_anzahl = ctk.CTkEntry(self.info_frame, placeholder_text="Anzahl")
        self.entry_anzahl.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Button zum Erzeugen des QR-Codes (ruft generate_qr_code auf)
        self.generate_button = ctk.CTkButton(self.info_frame, text="QR-Code erzeugen", command=self.generate_qr_code)
        self.generate_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

        # Frame für QR-Code-Anzeige
        self.vorschau_frame = ctk.CTkFrame(self)
        self.vorschau_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        # Platzhalter für den QR-Code
        self.qr_label = ctk.CTkLabel(self.vorschau_frame, text="Hier wird der QR-Code angezeigt")
        self.qr_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.vorschau_frame.grid_rowconfigure(0, weight=1)
        self.vorschau_frame.grid_columnconfigure(0, weight=1)

        # "Speichern"-Button
        self.save_button = ctk.CTkButton(self.vorschau_frame, text="Speichern", command=self.save_qr_code, state="disabled")  # Ausgegraut und funktionsunfähig wenn nicht alle Informationen angegeben sind
        self.save_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Frame für QR-Code-Scannen
        self.upload_frame = ctk.CTkFrame(self)
        self.upload_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # "QR-Code Bild hochladen"-Button
        self.upload_button = ctk.CTkButton(self.upload_frame, text="QR-Code Bild hochladen", command=self.upload_qr_image)
        self.upload_button.grid(row=0, column=0, padx=50, pady=75, sticky="NSEW")
        self.upload_frame.grid_rowconfigure(0, weight=1)
        self.upload_frame.grid_columnconfigure(0, weight=1)

        # Ergebnis Label
        self.result_label = ctk.CTkLabel(self.upload_frame, text="")
        self.result_label.grid(row=1, column=0, padx=10, pady=10)

    # Erstellen des QR Codes mit qrcode
    def generate_qr_code(self):
        titel = self.entry_titel.get()
        author = self.entry_author.get()
        untertitel = self.entry_untertitel.get()
        verlag = self.entry_verlag.get()
        auflage = self.entry_auflage.get()
        jahr = self.entry_jahr.get()
        kategorie = self.entry_kategorie.get()
        anzahl = self.entry_anzahl.get()

        if titel and author and verlag:
            # QR-Code Daten
            qr_data = f"Titel: {titel}, Author: {author}, Verlag: {verlag}, Edition: {auflage}, Year: {jahr}, Category: {kategorie}, Quantity: {anzahl}"

            # QR-Code generieren
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Bild im Speicher (BytesIO) speichern macht Vorschau möglich ohne zuvoriges lokales Speichern
            img = qr.make_image(fill="black", back_color="white")
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            bio.seek(0)

            # Bild für die Anzeige in Tkinter vorbereiten
            self.qr_image = Image.open(bio)

            # Verwende CTkImage, um das Bild auf High-DPI-Displays korrekt zu skalieren
            ctk_image = ctk.CTkImage(self.qr_image, size=(200, 200))

            # Bild im GUI anzeigen
            self.qr_label.configure(image=ctk_image)
            self.qr_label.image = ctk_image  # Verhindert das Bild von der Garbage Collection entfernt wird

            # "Speichern"-Button aktivieren
            self.save_button.configure(state="normal")

    # Speichern des QR-Codes auf dem System
    def save_qr_code(self):
        if self.qr_image:
            # Vordefinierter Dateiname aus dem Titel des Buches
            title = self.entry_titel.get()
            default_filename = f"{title}.png" if title else "QR_Code.png"

            # Datei-Dialog für das Speichern des Bildes mit dem vordefinierten Dateinamen
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=default_filename  # Vordefinierter Dateiname
            )

            if file_path:
                self.qr_image.save(file_path)
                print(f"QR-Code gespeichert unter: {file_path}")

    def upload_qr_image(self):
        file_types = [("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")]
        # Datei-Dialog zum Hochladen eines Bildes
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.scan_qr_code(file_path)

    def scan_qr_code(self, file_path):
        # QR-Code Informationen auslesen lassen
        img = cv2.imread(file_path)
        detector = cv2.QRCodeDetector()
        data, _, _ = detector(img)
        self.result_label.configure(text=data if data else "QR Code konnte nicht gelesen werden.")


# QRCodeApp Objekt
app = QRCodeApp()

# Mainloop
app.mainloop()