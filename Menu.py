import threading
import FaceRecognition


def Menu(building):
    def diffFloor():
        FaceRecognition.flag = False
        answer = int(input("Enter the floor number you wish to go"))
        building.moveElevator(answer)
        pass

    def conf():
        print("Configuration Menu:\n"
              "1) Add new Person\n"
              "2) Delete Person\n"
              "3) Edit Person\n"
              "4) Print all the residents\n"
              "5) Exit")

        x = int(input("Pick a number.\n"))
        switch = {
            "1": building.addResident,
            "2": building.deleteResident,
            "3": building.addResident,
            "4": building.printAllResidents,
            "5": "return"
        }
        if x not in range(1, 6):
            print("Wrong number! Choose again..\n")
            conf()
        else:
            out = switch[str(x)]
            if out is "return":
                return
            out()
            answer2 = input("Need anything else?").lower()
            if answer2 == "yes":
                conf()
            else:
                FaceRecognition.flag = True
                threading.Thread(target=FaceRecognition.compareThreadPersons, args=(building, ))
                return

    print("Menu: \n"
          "1) Go to different floor\n"
          "2) Configuration\n"
          "3) Shut down the system\n")

    menuSwitch = {
        "1": diffFloor,
        "2": conf,
        "3": "return"
    }

    while True:
        choice = input("Make a choice.\n")
        if choice == "1" or choice == "2" or choice=="3":
            break
        else:
            print("Wrong input!\n"
                  "Please choose again\n")

    answer = menuSwitch[choice]
    if answer is "return":
        return
    answer()
    # call the menu again till the system is shut down
    Menu(building)

