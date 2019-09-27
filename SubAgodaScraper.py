
# SubAgodaScraper class contain functions for scraping accommodation details on each accommodation Agoda page

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

import time
import dateutil.parser
from datetime import datetime
from datetime import timedelta
import datetime

import Accommodation
import Room

import AgodaKeys
import ConnectMongo
import GoogleCoordinates

class SubAgodaScraper(object):

    def __init__(self, subUrl):

        self.url = subUrl
        AgodaKeys.init()

        try:
            self.driver = webdriver.Firefox()
            self.delay = 30 # waiting for loading webpage
        except Exception as e:
            print("Error driver sub-agoda: ",e)

    def getURL(self):

        try:
            self.driver.get(self.url)
        except (TimeoutException,NoSuchElementException):
            print("No URL")

    def loadAgodaUrl(self):

        i = 1
        isContinue = True 

        while isContinue:

            totalHeight = self.driver.execute_script("return document.body.scrollHeight")
            currentLocation = 100 * i
            print("Location on screen ",currentLocation,"/",totalHeight)

            if currentLocation >= totalHeight:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                time.sleep(1)
                isContinue = False

            self.driver.execute_script(f"window.scrollTo(0, {currentLocation});") 
            i += 1
            time.sleep(1)
        
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            print("Loading Agoda URL")
        except TimeoutException:
            print("Loading Agoda URL: TimeoutException")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

    def extractIdInformations(self):

        try:
            idInformations = self.driver.find_element_by_class_name("PersonalizedRecommendationsCard--RecentHotelLink")
            accommodationId = idInformations.get_attribute(AgodaKeys.accomodationIdKey)
        
        except Exception as e: 
            accommodationId = ""
            print("Could not extract ID: ",e)

        return accommodationId

    def extractNameInformations(self):

        try:
            nameInformations = self.driver.find_element_by_class_name(AgodaKeys.accomodationName)
            name = nameInformations.text
        except Exception as e: 
            try:
                nameInformations = self.driver.find_elements_by_xpath('.//*[@data-selenium = "hotel-header-name"]')
                name = nameInformations[0].text
            except Exception as e: 
                name = ""
                print("Could not extract name: ",e)

        return name
        
    def extractAddressInformations(self):

        try:
            addressInformations = self.driver.find_elements_by_xpath(AgodaKeys.accomodationAddress)
            accommodationAddress = addressInformations[0].text
        except Exception as e: 
            accommodationAddress = ""
            print("Could not extract address Informations: ",e)

        return accommodationAddress
            
    def extractReviewScoreInformations(self):

        try:
            reviewScoreInformations = self.driver.find_element_by_class_name(AgodaKeys.accomodationReviewNumber)
            reviewScore = reviewScoreInformations.text

            reviewTotalScoreInformations = self.driver.find_element_by_class_name(AgodaKeys.accomodationReviewScore)
            totalReviewScore = reviewTotalScoreInformations.text

            joinText = 'Review: ' + reviewScore + '/10 From: ' + totalReviewScore

        except Exception as e:
            joinText = ""
            print("Could not extract review Informations: ",e)

        return joinText
       
    def extractUsefulInformations(self):

        try:
            usefulInformationsList = self.driver.find_element_by_id(AgodaKeys.accomodationUsefulInfo)
            usefulInformations = usefulInformationsList.text
        except Exception as e:
            usefulInformations = ""
            print("Could not extract useful Informations: ",e)

        return usefulInformations

    def extractAmountOfRoom(self, usefulInformations):

        roomText = usefulInformations.split("Number of rooms : ", 2)

        if len(roomText) > 1:
            amountRoomText = roomText[1].split("\n", 1)
            amountRoom = amountRoomText[0]
        else:
            amountRoom = 0
            print("Could not extract room inforations")

        return amountRoom

    def extractAmountOfFloor(self, usefulInformations):

        floorText = usefulInformations.split("Number of floors: ", 2)

        if len(floorText) > 1:
            amountFloorText = floorText[1].split("\n", 1)
            amountFloor = amountFloorText[0]
        else:
            amountFloor = 0
            print("Could not extract floor Informations")

        return amountFloor

    def extractYearEstablished(self, usefulInformations):

        yearText = usefulInformations.split("Year property opened: ", 2)

        if len(yearText) > 1:
            yearEstablishedText = yearText[1].split("\n", 1)
            yearEstablished = yearEstablishedText[0]
        else:
            yearEstablished = "-"
            print("Could not extract year of established")

        return yearEstablished

    def extractFeatureInformations(self):

        try:
            featureInformations = self.driver.find_element_by_class_name(AgodaKeys.accomodationFacilities)
            feature = featureInformations.text.replace('\n',' ')

        except Exception as e:
            feature = ""
            print("Could not extract feature Informations: ",e)
       
        return feature

    def extractPriceInformations(self):

        try:
            priceContainer = self.driver.find_element_by_class_name(AgodaKeys.accomodationPriceContainer)
            priceInformations = priceContainer.find_element_by_class_name(AgodaKeys.accomodationBestPrice)
            replaceCharacter = priceInformations.text.replace(',','')
            replaceCharacterUnit = replaceCharacter.replace('฿','')
            replaceSpace = replaceCharacterUnit.replace(' ','')
            roomPrice = replaceSpace

        except Exception as e:
            roomPrice = 0
            print("Could not extract price Informations: ",e)

        return roomPrice

    def extractTotalPriceInformations(self, roomPrice):

        try:
            priceContainer = self.driver.find_element_by_class_name(AgodaKeys.accomodationPriceContainer)
            priceInformations = priceContainer.find_element_by_class_name(AgodaKeys.accomodationTotalPrice)
            replaceCharacter = priceInformations.text.replace(',','')
            replaceCharacterUnit = replaceCharacter.replace('฿','')
            replaceSpace = replaceCharacterUnit.replace(' ','')
            roomTotalPrice = replaceSpace

        except Exception as e:
            roomTotalPrice = roomPrice
            print("Could not extract price Informations: ",e)

        return roomTotalPrice

    def extractRoomTypeInformations(self):

        try:
            roomTypeContainer = self.driver.find_element_by_class_name(AgodaKeys.accomodationRoomType)
            roomType = roomTypeContainer.text
        except Exception as e:
            roomType = ""
            print("Could not extract room type Informations: ",e)

        return roomType

    def extractSoldOut(self):
        
        try:
            soldoutInfo = self.driver.find_element_by_class_name(AgodaKeys.accomodationSoldOut)
            isSoldout = True
        except Exception as e:
            isSoldout = False
            print("Exception soldout: ",e)

        return isSoldout

    def extractRateStarInformations(self):

        try:

            rateInformations = self.driver.find_elements_by_xpath(AgodaKeys.accomodationRateStart)
            starRating = ""

            if len(rateInformations) > 0:

                starRating = rateInformations[0].get_attribute('class')    

                if 'star-15' in starRating:
                    starRating = 1.5
                elif 'star-25' in starRating:
                    starRating = 2.5
                elif 'star-35' in starRating:
                    starRating = 3.5
                elif 'star-45' in starRating:
                    starRating = 4.5
                elif 'star-1' in starRating:
                    starRating = 1
                elif 'star-2' in starRating:
                    starRating = 2
                elif 'star-3' in starRating:
                    starRating = 3
                elif 'star-4' in starRating:
                    starRating = 4           
                elif 'star-5' in starRating:
                    starRating = 5
                else:
                    starRating = 0

        except Exception as e:
            starRating = 0
            print("Could not extract start rating review Informations: ",e)

        return starRating

    def getCoordinate(self, address,selectedGoogleApiKey):

        try:
            
            keyLatitude = self.driver.find_elements_by_xpath(AgodaKeys.accomodationLatitude)
            keyLongitude = self.driver.find_elements_by_xpath(AgodaKeys.accomodationLongitude)
            latitude = keyLatitude[0].get_attribute('content')  
            longitude = keyLongitude[0].get_attribute('content')  
            coordinate = {'Latitude': latitude, 'Longitude': longitude} 

        except Exception as e:

            print("Exception location : ",e)
            
            try:
                googleCoordinate = GoogleCoordinates.GoogleCoordinates(address,selectedGoogleApiKey)
                coordinate = googleCoordinate.getCoordinateFromAddress()
            except Exception as e:
                coordinate = {'Latitude': 0, 'Longitude': 0} 
                print("Exception location : ",e)

        return coordinate  

    def closeDriver(self):

        if self.driver is not None:
            self.driver.close()