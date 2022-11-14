import smtplib
import imghdr
from email.message import EmailMessage

sender_email = 'kaikaipoon123@gmail.com'
receiver_email = 'kaikaipoon123@gmail.com'
password = 'bdhonhtvymmnivpj'  #app password for jarvis


newMessage = EmailMessage()
newMessage['Subject'] = "test email"
newMessage['From'] = sender_email
newMessage['To'] = receiver_email
newMessage.set_content('image attached')

with open('test.png', 'rb') as f:
    image_data = f.read()
    image_type = imghdr.what(f.name)
    image_name = f.name


newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()     #Identify ourselves with the mail server we are using.
    smtp.starttls() #Encrypt our connection
    smtp.ehlo()     #Reidentify our connection as encrypted with the mail server
    smtp.login(sender_email, password)
    smtp.send_message(newMessage)


