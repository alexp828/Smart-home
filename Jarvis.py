import speech_recognition as sr
import time
import threading
import pyttsx3
import socket
import requests, json
import numpy as np
from datetime import date, datetime
import cv2


def _NumtoMonth(MonthNum):
    return {
        1: "january",
        2: "february",
        3: "march",
        4: "april",
        5: "may",
        6: "june",
        7: "july",
        8: "august",
        9: "september",
        10: "october",
        11: "november",
        12: "december"
    }[MonthNum]


class speechRec:
    def __init__(self):
        self.speech_rec_obj = sr.Recognizer()
        self.speech_engine = pyttsx3.init()
        self.count = 0
        self.phrase = " "
        self.audio = None
        self.active = False
        self.exit = False

        while True:
            with sr.Microphone() as self.source:
                if self.count == 0:
                    self._calibration(self.source)
                    self.count += 1
                self._input_from_mic()
                self._classification()
                if self.exit:
                    self.speech_engine.say("Exiting program.")
                    self.speech_engine.runAndWait()
                    print("Program exited")
                    break

    def _calibration(self, audio):
        self.speech_engine.say("Calibration starts now")
        self.speech_engine.runAndWait()

        self.speech_rec_obj.adjust_for_ambient_noise(audio, duration=1)
        self.speech_engine.say("Calibration done")
        self.speech_engine.runAndWait()

    def _input_from_mic(self):
        print("speak")

        try:
            with sr.Microphone() as self.source:
                self.audio = self.speech_rec_obj.listen(self.source, timeout=2.5)

        except:
            pass


    def _classification(self):
        try:
            self.phrase = self.speech_rec_obj.recognize_google(self.audio)

            print(self.phrase)

            time.sleep(0.2)

            if self.active:

                if "weather" in self.phrase:
                    self._weather()

                if "today" in self.phrase and (" day" in self.phrase or "date" in self.phrase):
                    self._today()

                if "time" in self.phrase and ("now" in self.phrase or "today" in self.phrase):
                    self._time()

                if "shutdown" in self.phrase or "sleep" in self.phrase:
                    self._deactivation()

            else:
                if ("Jarvis" in self.phrase or "jarvis" in self.phrase) or "hey" in self.phrase or "wake" in self.phrase:
                    self._activation()

                if "exit" in self.phrase or "end" in self.phrase:
                    self.exit = True

        except :
            pass

    def _weather(self):
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        city_name = "San Jose"
        API_key = "e38204e90cf7b088f47a1f88ee1c6daf"
        URL = BASE_URL + "q=" + city_name + "&appid=" + API_key

        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperature = main['temp']
            humidity = main['humidity']

            self.speech_engine.say(f"Today's temperature is {np.round(temperature - 273)} , "
                                   f"Relative humidity is {np.round(humidity)} percent")
            self.speech_engine.runAndWait()

    def _NumtoWeek(self, weekNum):
        return {
            0: "monday",
            1: "tuesday",
            2: "wednesday",
            3: "thursday",
            4: "friday",
            5: "saturday",
            6: "sunday",
        }[weekNum]

    def _today(self):
        today = date.today()
        self.speech_engine.say(
            f"Today is {self._NumtoWeek(today.weekday())}, {_NumtoMonth(today.month)}, {today.day}")
        self.speech_engine.runAndWait()

    def _time(self):
        time_now = datetime.now()

        time_now_string = time_now.time().strftime("%I%M %p")

        if time_now_string[0] == "0":
            self.speech_engine.say(
                f"The time now is {time_now_string[1]} {time_now_string[2:4]} {time_now_string[5:7]}")
            self.speech_engine.runAndWait()

        else:
            self.speech_engine.say(
                f"The time now is {time_now_string[0:2]} {time_now_string[2:4]} {time_now_string[5:7]}")
            self.speech_engine.runAndWait()


    # def _sentry_mode(self):
    #
    # def human_classification(self, detection):
    #     for (x, y, w, h) in detection:
    #
    #         area_rec = w * h
    #
    #         if area_rec > 5000:
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #             return True
    #
    #         else:
    #             return False


    def _activation(self):
        self.speech_engine.say("Hello, Jarvis here.")
        self.speech_engine.runAndWait()
        self.active = True

    def _deactivation(self):
        self.speech_engine.say("Jarvis shutdown")
        self.speech_engine.runAndWait()
        self.active = False


if __name__ == "__main__":
    sp = speechRec()
