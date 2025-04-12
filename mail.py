import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
usuarios={
    "new":[],
    "old":[]
}
load_dotenv()
remitente = os.getenv('EMAIL_USER')
contraseña = os.getenv('EMAIL_PASS')

servidor_smtp = 'smtp.gmail.com'
puerto_smtp = 587

def sendMail(cuerpo, destinatario):
    mensaje = MIMEMultipart("alternative")
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Vacantes encontradas por el Crawler'
    parte_html = MIMEText(cuerpo, "html")
    mensaje.attach(parte_html)
    try:
        servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
        servidor.starttls()  # Iniciar la conexión segura
        servidor.login(remitente, contraseña)
        texto = mensaje.as_string()
        servidor.sendmail(remitente, destinatario, texto)
        print('Correo enviado exitosamente.')
    except Exception as e:
        print(f'Error al enviar el correo: {e}')
    finally:
        servidor.quit()






