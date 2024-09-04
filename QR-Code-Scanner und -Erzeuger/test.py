import qrcode

link = 'https://moodle.bildung-lsa.de/gym-scholl-magdeburg/pluginfile.php/108149/mod_resource/content/0/Projekt%203%20-%20QR-Code-Scanner%20und%20-Erzeuger.pdf'

qr_code = qrcode.make(link)

qr_code.save('Laurin_Faul.png')

print("QR-Code generated successfully")