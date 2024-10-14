from tkinter import filedialog, messagebox
import customtkinter as ctk
import qrcode
import cv2
from PIL import Image
import io


# Hauptklasse für die QR-Code Anwendung
class QRCodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("QR-Code Scanner und Generator")
        self.geometry("600x600")

        # Styling für modernes GUI
        ctk.set_appearance_mode("dark")  # Optionen: "dark", "light"
        ctk.set_default_color_theme("blue")  # Weitere Optionen: "green", "dark-blue"

        # Frame für QR-Code-Erzeugung
        self.generate_frame = ctk.CTkFrame(self)
        self.generate_frame.pack(pady=20)

        self.label_title = ctk.CTkLabel(self.generate_frame, text="Buchinformationen eingeben")
        self.label_title.grid(row=0, column=0, padx=10, pady=10)

        self.entry_title = ctk.CTkEntry(self.generate_frame, placeholder_text="Titel")
        self.entry_title.grid(row=1, column=0, padx=10, pady=10)

        self.entry_isbn = ctk.CTkEntry(self.generate_frame, placeholder_text="ISBN")
        self.entry_isbn.grid(row=2, column=0, padx=10, pady=10)

        self.entry_location = ctk.CTkEntry(self.generate_frame, placeholder_text="Standort")
        self.entry_location.grid(row=3, column=0, padx=10, pady=10)

        self.generate_button = ctk.CTkButton(self.generate_frame, text="QR-Code erzeugen",
                                             command=self.generate_qr_code)
        self.generate_button.grid(row=4, column=0, padx=10, pady=10)

        # Frame für QR-Code-Anzeige und Speicherung
        self.qr_frame = ctk.CTkFrame(self)
        self.qr_frame.pack(pady=20)

        self.qr_label = ctk.CTkLabel(self.qr_frame, text="Hier wird der QR-Code angezeigt")
        self.qr_label.grid(row=0, column=0, padx=10, pady=10)

        self.save_button = ctk.CTkButton(self.qr_frame, text="Speichern", command=self.save_qr_code, state="disabled")
        self.save_button.grid(row=1, column=0, padx=10, pady=10)

        # Variable zum Speichern des QR-Code-Bilds im Speicher
        self.qr_image = None

        # Frame für QR-Code-Scannen
        self.scan_frame = ctk.CTkFrame(self)
        self.scan_frame.pack(pady=20)

        self.upload_button = ctk.CTkButton(self.scan_frame, text="QR-Code Bild hochladen", command=self.upload_qr_image)
        self.upload_button.grid(row=0, column=0, padx=10, pady=10)

        self.result_label = ctk.CTkLabel(self.scan_frame, text="")
        self.result_label.grid(row=1, column=0, padx=10, pady=10)

    def generate_qr_code(self):
        title = self.entry_title.get()
        isbn = self.entry_isbn.get()
        location = self.entry_location.get()

        if title and isbn and location:
            # QR-Code Daten
            qr_data = f"Title: {title}, ISBN: {isbn}, Location: {location}"

            # QR-Code generieren
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)

            # Bild im Speicher (BytesIO) speichern
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

    def save_qr_code(self):
        if self.qr_image:
            # Vordefinierter Dateiname aus dem Titel des Buches
            title = self.entry_title.get()
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
        try:
            # Datei-Dialog zum Hochladen eines Bildes
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
            )

            if file_path:
                self.current_file = file_path

                # Lade das Bild mit PIL
                image = Image.open(self.current_file)
                image = image.resize((300, 300), Image.ANTIALIAS)  # Bild skalieren

                # Konvertiere das PIL-Image in ein CTkImage-Format, das in customtkinter verwendet werden kann
                tk_image = ctk.CTkImage(image, size=(300, 300))

                # Setze das Bild in der Label-Anzeige
                self.qr_label.configure(image=tk_image)
                self.qr_label.image = tk_image  # Referenz speichern, um das Bild anzuzeigen

                # Versuche, den QR-Code im hochgeladenen Bild zu scannen
                self.scan_qr_code(self.current_file)

        except Exception as e:
            # Fehlerbehandlung: Zeige eine Fehlermeldung, wenn etwas schiefgeht
            messagebox.showerror("Fehler",
                                 f"Beim Hochladen oder Verarbeiten des Bildes ist ein Fehler aufgetreten: {str(e)}")

    def scan_qr_code(self, file_path):
        # Bild mit OpenCV laden
        image = cv2.imread(file_path)

        # QR-Code dekodieren
        decoded_objects = cv2.QRCodeDetector()(image)

        if decoded_objects:
            # Wenn QR-Code gefunden wurde, den Text extrahieren
            data, points, _ = decoded_objects
            if points is not None:
                # Ergebnis anzeigen
                self.result_label.configure(text=f"QR-Code Inhalt:\n{data}")
        else:
            # Fehlermeldung, wenn kein QR-Code gefunden wurde
            messagebox.showerror("Fehler", "Kein QR-Code im Bild gefunden.")


# Anwendung starten
if __name__ == "__main__":
    app = QRCodeApp()
    app.mainloop()