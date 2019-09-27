
# Accommodation class is used for storing accommodation information as a object
# If you want to store more accommodation information, you need to add more variable in this class

class Accommodation:

    def __init__(self, accommodationId, name, location, latitude, longitude, rooms, floors, yearEstablished, yearClosed, reviewScore, starRating, facilities, accommodationUrl, accommodationType, createdAt, updatedAt):
        self.id = accommodationId
        self.name = name
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.rooms = rooms
        self.floors = floors
        self.yearEstablished = yearEstablished
        self.yearClosed = yearClosed
        self.reviewScore = reviewScore
        self.starRating = starRating
        self.facilities = facilities
        self.accommodationUrl = accommodationUrl
        self.accommodationType = accommodationType
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.printAcommodationInformations()

    def printAcommodationInformations(self):

        print("\n\n############# Acommodation: " + self.name + " ################\n")
        print("Acommodation Id: ", self.id)
        print("Name: ", self.name)        
        print("Address: ", self.location)
        print("Latitude: ", self.latitude)
        print("Longitude: ", self.longitude)
        print("Total Room: ", self.rooms)
        print("Total Floor: ", self.floors)
        print("Year Established: ", self.yearEstablished)
        print("Year Closed: ", self.yearClosed)
        print("ReviewScore: ", self.reviewScore)
        print("StarRating: ", self.starRating)
        print("Facilities: ", self.facilities)
        print("Accommodation Type: ", self.accommodationType)
        print("Accommodation Url: ", self.accommodationUrl)
        print("CreatedAt: ", self.createdAt)
        print("UpdatedAt: ", self.updatedAt)
        print("\n#####################################")