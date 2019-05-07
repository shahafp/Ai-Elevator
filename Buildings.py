import time
import os
import cv2

from Person import Person
import FaceRecognition


class Building:
    def __init__(self, numOfFloor, residents=None, encoderList=None):
        self.numOfResident = 0
        self.numOfFloor = numOfFloor
        self.elevator = 0
        self.ready = True
        if residents is None and encoderList is None:
            self.residents = []
            self.encoderList = []
        else:
            self.residents = residents
            self.encoderList = encoderList

    def addPerson(self, person):
        self.residents.append(person)
        self.encoderList.append(FaceRecognition.encodingImage(person.FirstName + " " + person.LastName))
        print("Successfully Added!")

    def addResident(self):
        name = input("Enter the name of the person(First Name): ").capitalize()
        last = input("Enter the name of the person(Last Name): ").capitalize()
        floor = int(input("Enter his floor"))
        person = Person(name, last, floor)
        self.residents.append(person)
        if not os.path.exists("./images/" + name + " " + last):
            os.mkdir("./images/" + name + " " + last)
        cam = cv2.VideoCapture(0)
        for i in range(1):
            val, image = cam.read()
            cv2.imwrite("./images/" + name + " " + last + "/" + name + " " + last + '.jpg', image)
        cam.release()
        self.encoderList.append(FaceRecognition.encodingImage(person.FirstName + " " + person.LastName))
        print("Successfully Added!")

    def deleteResident(self):
        name = input("Enter the name of the person(First Name): ").capitalize()
        last = input("Enter the name of the person(Last Name): ").capitalize()

        for p in self.residents:
            if p.FirstName == name and p.LastName == last:
                self.residents.remove(p)
                self.encoderList.remove(FaceRecognition.encodingImage(p.FirstName + " " + p.LastName))

    def editResident(self):
        pass

    def printAllResidents(self):
        for p in self.residents:
            print("Resident name: {} {} in Floor #{}".format(p.FirstName, p.LastName, p.floor))

    def moveElevator(self, personList):
        self.ready = False
        for person in personList:
            while self.elevator < person.floor + 1:
                print(str(self.elevator) + ' ▲ ')
                time.sleep(2)
                self.elevator += 1
            print("Elevator has arrive to floor # {}".format(self.elevator))
            time.sleep(1)
        time.sleep(1)
        print("Elevator goes to floor 0")
        self.moveElevatorDown()

    def moveElevatorDown(self):
        while self.elevator > 0:
            print(str(self.elevator) + ' ▼ ')
            time.sleep(2)
            self.elevator -= 1
        print("0 ▼ \n"
              "Elevator is ready for use")
        self.ready = True
