import cv2
import numpy as np
import nexmo
import time
import smtplib
import imghdr
from email.message import EmailMessage

def human_classification(detection):
    for (x, y, w, h) in detection:

        area_rec = w * h

        if area_rec > 5000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return True

        else:
            return False

def send_email(text, image):
    sender_email = 'kaikaipoon123@gmail.com'
    receiver_email = 'kaikaipoon123@gmail.com'
    password = 'bdhonhtvymmnivpj'  # app password for jarvis

    newMessage = EmailMessage()
    newMessage['Subject'] = "Human detected outside of home!"
    newMessage['From'] = sender_email
    newMessage['To'] = receiver_email
    newMessage.set_content(text)

    with open(image, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()  # Identify ourselves with the mail server we are using.
        smtp.starttls()  # Encrypt our connection
        smtp.ehlo()  # Reidentify our connection as encrypted with the mail server
        smtp.login(sender_email, password)
        smtp.send_message(newMessage)


cap = cv2.VideoCapture(1)
client_nexmo = nexmo.Client(key='9768791e', secret='LQF3kbL6grfKJq5o')

classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

human_detected = False
time_reference = time.time()
state = 0  # state == 1: either person or false detection, state == 2: person is detected SMS is sent
count = 0
detection_time = 2  # time it takes to

while True:
    time_current = time.time()
    ret, frame = cap.read()

    # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray_frame = cv2.flip(gray_frame, 1)


    persons_detected = classifier.detectMultiScale(frame, 1.3, 5)

    if state == 0:
        detection = human_classification(persons_detected)

        if detection:
            time_reference = time.time()
            state = 1

    if state == 1:
        detection = human_classification(persons_detected)

        if detection:
            # human is for sure detected if detected more than 2 seconds
            if time_current - time_reference >= detection_time:
                state = 2
                time_reference = time.time()

        else:
            time_reference = time.time()
            state = 0

    if state == 2:
        detection = human_classification(persons_detected)
        text = 'Security breach! Image attached.'
        cv2.imwrite(f'human_detected_{count}.png', frame)
        picture = f'human_detected_{count}.png'
        count += 1
        send_email(text, picture)

        time_reference = time.time()
        state = 3

    if state == 3:
        if time_current - time_reference <= 15*60:
            state = 3

        else:
            state = 0
            time_reference = time.time()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

