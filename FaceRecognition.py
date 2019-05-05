import threading
import _thread
import time
import face_recognition
import lock as lock
from PIL import Image, ImageDraw
import cv2
import Buildings
from Person import Person
from Person import Manager

flag = True


def encodingImage(name):
    # Image 1
    image_of_person = face_recognition.load_image_file('./images/' + name + '/' + name + '.jpg')

    # The encoding function return array and we need only the first column
    face_encoding = face_recognition.face_encodings(image_of_person)[0]

    return face_encoding


def comparePersons(persons, encodings):
    p = Person()
    cam = cv2.VideoCapture(0)
    for i in range(1):
        val, image = cam.read()
        cv2.imwrite("./images/" + str(i) + '.jpg', image)
    cam.release()
    cv2.destroyAllWindows()

    # Load test image to find face in
    test_image = face_recognition.load_image_file('./images/' + str(i) + '.jpg')

    # Find face in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    # Convert to PIL format
    pil_image = Image.fromarray(test_image)

    # Create a ImageDraw instance
    draw = ImageDraw.Draw(pil_image)

    # Loop through faces in test image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(encodings, face_encoding)

        name = Person()

        if True in matches:
            first_match_index = matches.index(True)
            name = persons[first_match_index]

        if name.FirstName is not None:
            p = name

    del draw

    # Display image
    # pil_image.show()

    return p


def compareThreadPersons(building):
    # Let the person decide if he wants a different floor
    time.sleep(3)

    p = Person()
    cam = cv2.VideoCapture(0)
    while flag:
        defined = False
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
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(building.encoderList, face_encoding)

            name = Person()

            if True in matches:
                first_match_index = matches.index(True)
                name = building.residents[first_match_index]

            if name.FirstName is not None:
                if p.FirstName == name.FirstName and p.LastName == name.LastName:
                    defined = True
                p = name

        del draw

        if isinstance(p, Manager):
            break

        if p.FirstName is not None and not defined:
            # If the camera identify new person it checks if the elevator is ready for use
            if building.ready:
                sendFromThread(p, building)

        else:
            continue

        # Display the resulting frame
        # cv2.imshow('frame', image)
        if cv2.waitKey(20) & 0XFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def sendFromThread(person, building):
    if person is None:
        print("No Person found")
    else:
        print("Hi " + person.FirstName + " " + person.LastName + " " + "going up to floor {} ".format(person.floor))
        building.moveElevator(person.floor)
