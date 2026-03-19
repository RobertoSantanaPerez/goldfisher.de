#!/usr/bin/python3

import smtplib
from email.message import EmailMessage

# E-Mail-Inhalt erstellen
msg = EmailMessage()
msg['Subject'] = 'Test-E-Mail von Python'
msg['From'] = 'roberto.santana.berlin@gmail.com'
msg['To'] = 'roberto.santana.berlin@gmail.com'
msg.set_content('Hallo, dies ist eine Test-E-Mail, die mit Python versendet wurde!')

# Verbindung zu Gmail SMTP
smtp_server = 'smtp.gmail.com'
smtp_port = 465  # SSL-Port

# Dein App-Passwort hier einfügen
gmail_user = 'roberto.santana.berlin@gmail.com'
gmail_app_password = 'woim qdex xlhe skdg'

# E-Mail senden
with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(gmail_user, gmail_app_password)
    server.send_message(msg)

print("E-Mail erfolgreich gesendet!")
