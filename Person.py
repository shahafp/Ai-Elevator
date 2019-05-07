
class Person:

    def __init__(self, firstname=None, lastname=None, floor=None):
        self.FirstName = firstname
        self.LastName = lastname
        self.floor = floor
        self.defined = False

    def __str__(self):
        return "First Name: {} Last Name: {} In Floor {}".format(self.FirstName,self.LastName, self.floor)

    def editPerson(self):
        pass

    def equal(self,person):
        if self.FirstName == person.FirstName and self.LastName == person.LastName:
            return True
        return False


class Manager(Person):

    def __init__(self, firstname, lastname):
        super().__init__(firstname, lastname)

    def __str__(self):
        return "Name: " + self.FirstName + " " + self.LastName + " - Manger"
