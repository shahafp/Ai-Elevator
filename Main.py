from Person import Person, Manager
import Buildings
import Menu
import FaceRecognition
import threading
import time
import pyttsx3
import pickle

if __name__ == '__main__':

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'english+f3')
    engine.setProperty('rate', 120)  # 120 words per minute
    engine.setProperty('volume', 0.5)
    engine.say("welcome!")
    engine.runAndWait()

    Shahaf = Manager("Shahaf", "Pariente")
    Meidan = Person("Meidan", "Nasi", 2)
    Guy = Person("Guy", "Yanko", 3)
    Oron = Person("Oron", "Pariente", 5)
    Dana = Person("Dana", "Avraham", 1)

    personList = [Shahaf, Meidan, Guy, Oron, Dana]

    with open("Residents.pk1", "wb") as output:
        pickle.dump(personList, output, pickle.HIGHEST_PROTOCOL)

    personList = []

    with open("Residents.pk1", "rb+") as output:
        personList = pickle.load(output)

    b1 = Buildings.Building(9)
    # b1.addList(personList)
    for person in personList:
        b1.addPerson(person)

    # Thread to the camera
    x = threading.Thread(target=FaceRecognition.compareThreadPersons, args=(b1,))
    x.start()

    Menu.Menu(b1)

    # allow the thread break out from the while loop
    FaceRecognition.flag = False
    # sleep is to give the thread time to work
    time.sleep(1)


