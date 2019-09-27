
# ConnectMongo class is used for connecting to MongoDB cloud server
# https://cloud.mongodb.com

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse

from itertools import groupby
import dateutil.parser
import datetime

import Accommodation
import Room

class Connector(object):

    def __init__(self):

        # if you want to connect to test server please set isUsingTestServer = True
        isUsingTestServer = False

        if isUsingTestServer:
            # create connection to localhost
            con=MongoClient("localhost",27017)
            # connect database agoda
            db=con.get_database("AgodaScraper") 
            # create collection 
            self.accommodations = db.Accommodations
            self.rooms = db.Rooms
            self.roomsWithOutReplacingInfo = db.RoomsWithoutReplacingInfo

        else:
            # create connection to server
            con = MongoClient("mongodb+srv://webScraper:webScraper@agodascraper-jqlci.mongodb.net/test?retryWrites=true&w=majority")
            db=con.admin
            serverStatusResult=db.command("serverStatus")
            print("Status Server: ",serverStatusResult)

            db=con.get_database("AgodaScraper")
            self.accommodations = db.Accommodations
            self.rooms = db.Rooms
            self.roomsWithOutReplacingInfo = db.RoomsWithoutReplacingInfo

    # this method is used for insert or update accomodation informations to accommodotion collect
    def insertAccommodationInformations(self, accommodationObj):

            if self.accommodations.find({'AccommodationId': accommodationObj.id, "accommodationType": accommodationObj.accommodationType}).count() > 0:
                print("Update Accommodation")
            # update document 
                self.accommodations.find_one_and_update({ "accommodationId": accommodationObj.id }, {'$set': {"accommodationId": accommodationObj.id,
                "reviewScore": accommodationObj.reviewScore,
                "starRating": accommodationObj.starRating,
                "facilities": accommodationObj.facilities,
                "accommodationUrl": accommodationObj.accommodationUrl,
                "createdAt": accommodationObj.createdAt,
                "lastModified": accommodationObj.updatedAt,
                "accommodationType": accommodationObj.accommodationType
                }})

            else: 

            # insert document
                print("Insert Accommodation")

                self.accommodations.insert_one({"accommodationId": accommodationObj.id,
                "name": accommodationObj.name,
                "address": accommodationObj.location,
                "latitude": accommodationObj.latitude,
                "longitude": accommodationObj.longitude,
                "rooms": int(accommodationObj.rooms),
                "floors": int(accommodationObj.floors),
                "yearEstablished": accommodationObj.yearEstablished,
                "yearClosed": accommodationObj.yearClosed,
                "reviewScore": accommodationObj.reviewScore,
                "starRating": int(accommodationObj.starRating),
                "facilities": accommodationObj.facilities,
                "accommodationUrl": accommodationObj.accommodationUrl,
                "accommodationType": accommodationObj.accommodationType,
                "createdAt": accommodationObj.createdAt,
                "lastModified": accommodationObj.updatedAt,
                })

    # this method is used for insert or update room informations to room collection
    def insertRoomInformations(self, roomObj):

            if roomObj.checkInDate is not datetime.date:
                newDateFormat = roomObj.checkInDate.strftime("%Y-%m-%d'T'00:00:00.000+00:00")
                newDate = dateutil.parser.parse(str(newDateFormat))
            else:
                newDate = roomObj.checkInDate

            if self.rooms.find({'accommodationId': roomObj.id, "checkInDate": newDate}).count() > 0:
                print("UPDATE ROOMs: ",roomObj.id,roomObj.name,int(roomObj.bestPrice),int(roomObj.totalPrice),roomObj.soldOut,newDate)
                # update document 
                self.rooms.find_one_and_update({'accommodationId': roomObj.id, "checkInDate": newDate}, {'$set': {"accommodationId": roomObj.id,
                "name": roomObj.name,
                "bestPrice": int(roomObj.bestPrice),
                "totalPrice": int(roomObj.totalPrice),
                "soldOut": roomObj.soldOut,
                "roomType": roomObj.roomType,
                "createdAt": roomObj.createdAt,
                "checkInDate": newDate
                }})

            else: 
                print("INSERT ROOMs: ",roomObj.id,roomObj.name,int(roomObj.bestPrice),int(roomObj.totalPrice),roomObj.soldOut,newDate)
                # insert document
                self.rooms.insert_one({"accommodationId": roomObj.id,
                "name": roomObj.name,
                "bestPrice": int(roomObj.bestPrice),
                "totalPrice": int(roomObj.totalPrice),
                "soldOut": roomObj.soldOut,
                "roomType": roomObj.roomType,
                "createdAt": roomObj.createdAt,
                "checkInDate": newDate
                })

    # this method always inserting room informations to RoomsWithoutReplacingInfo collection
    def insertRoomWithoutReplacingInfo(self, roomObj):

            if roomObj.checkInDate is not datetime.date:
                newDateFormat = roomObj.checkInDate.strftime("%Y-%m-%d'T'00:00:00.000+00:00")
                newDate = dateutil.parser.parse(str(newDateFormat))
            else:
                newDate = roomObj.checkInDate

            self.roomsWithOutReplacingInfo.insert_one({"accommodationId": roomObj.id,
            "name": roomObj.name,
            "bestPrice": int(roomObj.bestPrice),
            "totalPrice": int(roomObj.totalPrice),
            "soldOut": roomObj.soldOut,
            "roomType": roomObj.roomType,
            "createdAt": roomObj.createdAt,
            "checkInDate": newDate
            })

    def getAccommodationInformationsById(self, accommodationId):
        accommodationInfo = self.accommodations.find_one({ "accommodationId": accommodationId})
        return accommodationInfo

    def getAccommodationInformationsByName(self, name):
        accommodationInfo = self.accommodations.find_one({ "name": name})
        return accommodationInfo

    def getRoomObjsBySpecificKeyAndValue(self, key, value):
        return  self.rooms.find({ key : value })

    def getRoomObjsWithMultipleSpecificKeyAndValue(self, key1, value1, key2, value2):
        return  self.rooms.find({ key1 : value1 , key2 : value2 })
        
    def convertStringToIntegerWithSpecificObject(self, key, existingValue, newValue):

        if self.rooms.find({key: existingValue}).count() > 0:
            
            self.rooms.find_one_and_update({ key: existingValue }, {'$set': {
            key: newValue
            }})

        else:
            print("not found")

    # this metond is used for getting amount of accommodations in each check in date 
    def getAmountsOfAccommodationInEachDate(self):

        checkInDateList = []
        allrooms = self.getAllRoomObjects()

        for room in allrooms:
            checkInDate = room['checkInDate']
            checkInDateList.append(checkInDate)
            
        # remove duplicate 
        removeDuplicateList = self.removeDuplicatedList(checkInDateList)
        checkInObjects = self.countOfDuplicatedItems(checkInDateList,removeDuplicateList)   

        return checkInObjects

    def getAllAccommodationObjects(self):
        return self.accommodations.find().sort("checkInDate",pymongo.ASCENDING)

    def getAllRoomObjects(self):
        return self.rooms.find().sort("checkInDate",pymongo.ASCENDING)

    def removeDuplicatedList(self, allCheckInDateList):
        removeDuplicateList = list(dict.fromkeys(allCheckInDateList))
        return removeDuplicateList

    def removeDuplicatedRecord(self):

        cursor = self.rooms.aggregate(
            [
                {"$group": {"_id": { "firstField": "$accommodationId", "secondField": "$checkInDate" }, "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
                {"$match": {"count": { "$gte": 2 }}}
            ]
        )

        response = []
        for doc in cursor:
            del doc["unique_ids"][0]
            for id in doc["unique_ids"]:
                response.append(id)

        self.rooms.remove({"_id": {"$in": response}})

    def countOfDuplicatedItems(self, allDuplicatedCheckInDateItems, removeDuplicatedItems):

        newList = []

        for item in removeDuplicatedItems:
            obj = dict()
            obj['date'] = item
            obj['amount'] = allDuplicatedCheckInDateItems.count(item)
            newObject = (obj)
            newList.append(newObject)

        return newList

    def removeObjectById(self, objId):
        self.rooms.remove({'_id': ObjectId(objId)})
