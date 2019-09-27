
# Room class is used for storing room price information as a object
# If you want to store more room information, you need to add more variable in this class

class Room:

    def __init__(self, acommodationId, name, bestPrice, totalPrice, roomType, soldOut, createdAt, checkInDate):
        self.id = acommodationId
        self.name = name
        self.bestPrice = bestPrice
        self.totalPrice = totalPrice
        self.roomType = roomType
        self.soldOut = soldOut
        self.createdAt = createdAt
        self.checkInDate = checkInDate

        self.printAcommodationInformations()

    def printAcommodationInformations(self):

        print("\n\n############# Acommodation " + self.name + " ################\n")
        print("Acommodation Id: ", self.id)
        print("Name: ", self.name)        
        print("Best Price: ", self.bestPrice)
        print("Total Price: ", self.totalPrice)
        print("Room Type: ", self.roomType)
        print("Is Sould Out: ", self.soldOut)
        print("Created At: ", self.createdAt)
        print("Check In Date: ", self.checkInDate)
        print("\n#####################################")
