from Person import Person, Manager
import Buildings
import Menu
import FaceRecognition
import threading
import time
import pyttsx3

if __name__ == '__main__':

    # engine = pyttsx3.init()
    # engine.say("Hello and welcome!")
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)
    # engine.setProperty('rate', 120)  # 120 words per minute
    # engine.setProperty('volume', 0.5)
    # engine.runAndWait()

    Shahaf = Manager("Shahaf", "Pariente")
    Meidan = Person("Meidan", "Nasi", 2)
    Guy = Person("Guy", "Yanko", 3)
    Oron = Person("Oron", "Pariente", 5)
    Dana = Person("Dana", "Avraham", 1)

    b1 = Buildings.Building(9)
    b1.addPerson(Shahaf)
    b1.addPerson(Meidan)
    b1.addPerson(Oron)
    b1.addPerson(Dana)
    b1.addPerson(Guy)

    # Thread to the camera
    x = threading.Thread(target=FaceRecognition.compareThreadPersons, args=(b1,))
    x.start()

    Menu.Menu(b1)

    # allow the thread break out from the while loop
    FaceRecognition.flag = False
    # sleep is to give the thread time to work
    time.sleep(1)


