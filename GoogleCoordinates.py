import requests

class GoogleCoordinates(object):

    def __init__(self, address, apiKey):

        self.address = address 
        self.apiKey = apiKey
        #"AIzaSyC1njH8lej4HcvxJFBIIRFW4iLgbqx_NnM"

    def getCoordinateFromAddress(self):

        apiResponse = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(self.address, self.apiKey))
        apiResponseDict = apiResponse.json()

        if apiResponseDict['status'] == 'OK':
            latitude = apiResponseDict['results'][0]['geometry']['location']['lat']
            longitude = apiResponseDict['results'][0]['geometry']['location']['lng']
            return {'Latitude': latitude, 'Longitude': longitude}
        else:
            return {'Latitude': 0, 'Longitude': 0}
