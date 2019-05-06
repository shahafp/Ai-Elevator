import os
import time
import face_recognition
from PIL import Image, ImageDraw
import cv2
from Person import Manager

flag = True


def encodingImage(name):
    # Image 1
    image_of_person = face_recognition.load_image_file('./images/' + name + '/' + name + '.jpg')

    # The encoding function return array and we need only the first column
    face_encoding = face_recognition.face_encodings(image_of_person)[0]

    return face_encoding


def compareThreadPersons(building):

    # params:
    # building - the specific building we work on

    # Let the person decide if he wants a different floor
    time.sleep(3)

    person = None  # Specific person in the picture
    personList = []  # List of person, In case there are more than 1 person in front of the camera

    cam = cv2.VideoCapture(0)  # Open the camera

    while flag:  # Flag is controlled by the menu.
        val, image = cam.read()
        cv2.imwrite('./images/person.jpg', image)

        # Load test image to find face in
        test_image = face_recognition.load_image_file('./images/person.jpg')

        # Find face in test image
        face_locations = face_recognition.face_locations(test_image)
        face_encodings = face_recognition.face_encodings(test_image, face_locations)

        # Convert to PIL format
        pil_image = Image.fromarray(test_image)

        # Create a ImageDraw instance
        draw = ImageDraw.Draw(pil_image)

        # Loop through faces in test image
        for (_, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(building.encoderList, face_encoding)

            name = None

            if True in matches:
                first_match_index = matches.index(True)
                name = building.residents[first_match_index]

            # If statement to check if the person in from of the camera is already recognized.
            if name is not None:
                if person is not None and person.FirstName == name.FirstName and person.LastName == name.LastName:
                    person.defined = True
                personList.append(name)
                person = name

        del draw

        # Delete the taken pic after taking her to use the compare func
        try:
            os.remove('./images/person.jpg')
        except os.error:
            print('error')

        # If the person in front of the camera is manager we pass the recognition part to let him work on the elevator
        if isinstance(person, Manager):
            break

        # Checking if the camera did recognize a person and if this person has not just recognized
        if person and not person.defined:
            # If the camera identify new person it checks if the elevator is ready for use
            if building.ready:
                sendFromThread(personList, building)
                personList = []  # After we done with all the persons in the elevator

        else:
            continue

        # Display the resulting frame
        # cv2.imshow('frame', image)
        if cv2.waitKey(20) & 0XFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def sendFromThread(personList, building):
    found = False
    for person in personList:
        if person is None:
            print("No Person found")
        else:
            found = True
            print("Hi " + person.FirstName + " " + person.LastName + " " + "going up to floor {} ".format(person.floor))
    if found:
        building.moveElevator(personList)
