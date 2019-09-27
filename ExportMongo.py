
# ExportMongo class is used for exporting data from Mongo database to excel file (.CSV)

import pandas as pd
from pymongo import MongoClient
import desktop

class Exporter(object):

    def __init__(self):

        # if you want to connect to test server please set isUsingTestServer = True
        isUsingTestServer = False

        if isUsingTestServer:
            # create connection in localhost
            con=MongoClient("localhost",27017)
            # connect database AgodaScraper
            db=con.get_database("AgodaScraper") 
            # create collection 
            self.accommodations = db.Accommodations
            self.rooms = db.Rooms
            self.roomsWithOutReplacingInfo = db.RoomsWithoutReplacingInfo
            
        else:
            # create connection
            con = MongoClient("mongodb+srv://webScraper:webScraper@agodascraper-jqlci.mongodb.net/test?retryWrites=true&w=majority")
            db=con.admin
            # Issue the serverStatus command and print the results
            serverStatusResult=db.command("serverStatus")
            print("Status Server: ",serverStatusResult)

            db=con.get_database("AgodaScraper")
            # create collection (table)
            self.accommodations = db.Accommodations
            self.rooms = db.Rooms
            self.roomsWithOutReplacingInfo = db.RoomsWithoutReplacingInfo

    def exportAccommodationObjectsFromMongoToCSV(self, date):

        cursor = self.accommodations.find()
        dictArr = []

        for accommodation in list(cursor):

            accommodationId = accommodation["accommodationId"]
            name = accommodation["name"]
            address = accommodation["address"]
            latitude = accommodation["latitude"]
            longitude = accommodation["longitude"]
            reviewScore = accommodation["reviewScore"]
            starRating = accommodation["starRating"]
            rooms = accommodation["rooms"]
            floors = accommodation["floors"]
            facilities = accommodation["facilities"]
            accommodationType = accommodation["accommodationType"]
            yearEstablished = accommodation["yearEstablished"]
            yearClosed = accommodation["yearClosed"]

            createdAt = accommodation["createdAt"]
            cratedAtStr = createdAt.strftime('%d/%m/%Y')
            lastModified = accommodation["lastModified"]
            lastModifiedStr = lastModified.strftime('%d/%m/%Y')
            
            dictArr.append({'accommodationId': accommodationId, 'name': name, 'address': address, 'latitude': latitude, 'longitude': longitude, "review": reviewScore, "starRating": starRating, "rooms": rooms, "floors": floors, "facilities": facilities, "type": accommodationType, "yearEstablished": yearEstablished, "yearClosed": yearClosed, "cratedAt": cratedAtStr, "lastModified": lastModifiedStr})

        sortingColum = ['accommodationId','name','address','latitude','longitude','review','starRating','rooms','floors','facilities','type','yearEstablished','yearClosed','cratedAt','lastModified']

        df =  pd.DataFrame(dictArr)
        
        # sorting column in excel following sortingColum list
        df.loc[:,sortingColum].to_csv(('{}{}{}'.format('ข้อมูลที่พัก_',date,'.csv')))
        desktop.open('{}{}{}'.format('ข้อมูลที่พัก_',date,'.csv'))

    def exportRoomObjectsFromMongoToCSV(self, date):

        cursor = self.rooms.find()
        dictArr = []

        for accommodation in list(cursor):

            accommodationId = accommodation["accommodationId"]
            name = accommodation["name"]
            roomType = accommodation["roomType"]
            bestPrice = accommodation["bestPrice"]
            totalPrice = accommodation["totalPrice"]
            soldOut = accommodation["soldOut"]

            createdAt = accommodation["createdAt"]
            cratedAtStr = createdAt.strftime('%d/%m/%Y')

            checkInDate = accommodation["checkInDate"]
            checkInDateStr = checkInDate.strftime('%d/%m/%Y')
            
            dictArr.append({'accommodationId': accommodationId, 'name': name, "roomType": roomType, "bestPrice": bestPrice, "totalPrice": totalPrice, "soldOut": soldOut, "checkInDate": checkInDateStr, "cratedAt": cratedAtStr})

        sortingColum = ['accommodationId','name','roomType','bestPrice','totalPrice','soldOut','checkInDate','cratedAt']

        df =  pd.DataFrame(dictArr)
        df.loc[:,sortingColum].to_csv(('{}{}{}'.format('ข้อมูลราคาห้องพัก_',date,'.csv')))
        desktop.open('{}{}{}'.format('ข้อมูลราคาห้องพัก_',date,'.csv'))

    def exportRoomWithoutReplacingInfoObjectsFromMongoToCSV(self, date):
        cursor = self.roomsWithOutReplacingInfo.find()
        dictArr = []

        for accommodation in list(cursor):

            accommodationId = accommodation["accommodationId"]
            name = accommodation["name"]
            roomType = accommodation["roomType"]
            bestPrice = accommodation["bestPrice"]
            totalPrice = accommodation["totalPrice"]
            soldOut = accommodation["soldOut"]

            createdAt = accommodation["createdAt"]
            cratedAtStr = createdAt.strftime('%d/%m/%Y')

            checkInDate = accommodation["checkInDate"]
            checkInDateStr = checkInDate.strftime('%d/%m/%Y')
            
            dictArr.append({'accommodationId': accommodationId, 'name': name, "roomType": roomType, "bestPrice": bestPrice, "totalPrice": totalPrice, "soldOut": soldOut, "checkInDate": checkInDateStr, "cratedAt": cratedAtStr})

        sortingColum = ['accommodationId','name','roomType','bestPrice','totalPrice','soldOut','checkInDate','cratedAt']

        df =  pd.DataFrame(dictArr)
        df.loc[:,sortingColum](('{}{}{}'.format('ข้อมูลราคาห้องพักทั้งหมด_',date,'.csv')))
        desktop.open('{}{}{}'.format('ข้อมูลราคาห้องพักทั้งหมด_',date,'.csv'))