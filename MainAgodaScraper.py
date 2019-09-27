
# MainAgoda class contain functions for scraping accommodation details on main Agoda page

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
import SubAgodaScraper
import ConnectMongo
import GoogleCoordinates

class MainAgodaScraper(object):

    def __init__(self, mainUrl):

        self.url = mainUrl
        self.driver = webdriver.Firefox()

        # waiting for loading webpage
        self.delay = 30 
        AgodaKeys.init()

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
            currentLocation = 200 * i
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


    def loadUrlNextPage(self):

        try:
            element = self.driver.find_element_by_class_name(AgodaKeys.nextPage)
            self.driver.execute_script("arguments[0].click();", element)
            currentURL = self.driver.current_url

        except Exception as e:
            print("Could not load URL for next page")
            currentURL = ""
            print("Exception next page: ",e)
            self.driver.close()

        return currentURL

    # create accommodation URL by using accommodatin id
    def createAccommodationURLFromId(self, accommodationId):
  
        try:
            urlPost = self.driver.find_element_by_id(f"hotel-{accommodationId}-container")
            accommodationURL = urlPost.get_attribute('href')
        except NoSuchElementException:
            accommodationURL = ""
            print("Could not find accommodation URL")
            self.driver.close()

        return accommodationURL

    # extract accommodation details
    def extractInformations(self, checkInDateStr, googleApiKey, accommodationType):
            
        agodaDB = ConnectMongo.Connector()    

        try:
        
            accommodationList = self.driver.find_elements_by_xpath('.//*[@data-selenium = "hotel-item"]')
            print("Total Accommodation List in This Page: ",len(accommodationList))

            # scraping accommodation Informations and loop until reaching last accommodation
            for accommodation in accommodationList:

                # create dataCreatedAt and dataUpdatedAt from current time
                dateAndTime = datetime.datetime.now()

                dataCreatedAt = dateAndTime
                dataUpdatedAt = dateAndTime
                checkInDate = dateutil.parser.parse(str(checkInDateStr))

                try:

                    accommodationId = accommodation.get_attribute(AgodaKeys.accomodationIdKey)
                    accommodationURL = self.createAccommodationURLFromId(accommodationId)
                    
                    subScrapper = SubAgodaScraper.SubAgodaScraper(accommodationURL)
                    subScrapper.getURL()
                    subScrapper.loadAgodaUrl()

                    # ------ start scraping accommodation Informations ------- #

                    name = subScrapper.extractNameInformations()

                    # verify if this accommondation is Nida, program will skip for scraping data
                    if "nida" in name.lower():
                        continue

                    address = subScrapper.extractAddressInformations()
                    roomBestPrice = subScrapper.extractPriceInformations()
                    roomTotalPrice = subScrapper.extractTotalPriceInformations(roomBestPrice)
                    roomType = subScrapper.extractRoomTypeInformations()
                    accommodationRateStar = subScrapper.extractRateStarInformations()

                    # using google map to get latitude and longitude by using address 
                    coordinate = subScrapper.getCoordinate(address, googleApiKey)
                    latitude = coordinate["Latitude"]
                    longitude = coordinate["Longitude"]

                    reviewScore = subScrapper.extractReviewScoreInformations()
                    usefulInformations = subScrapper.extractUsefulInformations()
                    amountRoom = subScrapper.extractAmountOfRoom(usefulInformations)
                    amountFloor = subScrapper.extractAmountOfFloor(usefulInformations)
                    yearEstablished = subScrapper.extractYearEstablished(usefulInformations)
                    feature = subScrapper.extractFeatureInformations()
                    isSoldOut = subScrapper.extractSoldOut()
                    # saving data to mongoDB with Accommodation collection
                    accommodationObj = Accommodation.Accommodation(accommodationId, name, address, latitude, longitude, amountRoom, amountFloor, yearEstablished,"-", reviewScore, accommodationRateStar, feature, accommodationURL, accommodationType, dataCreatedAt, dataUpdatedAt)
                    agodaDB.insertAccommodationInformations(accommodationObj)

                    # saving data to mongoDB with Room collection
                    roomObj = Room.Room(accommodationId, name, roomBestPrice, roomTotalPrice, roomType, isSoldOut, dataCreatedAt, checkInDate)
                    agodaDB.insertRoomInformations(roomObj)
                    agodaDB.insertRoomWithoutReplacingInfo(roomObj)
                    subScrapper.closeDriver()

                except Exception as e:
                    subScrapper.closeDriver()
                    print("Exception close driver: ",e)

        except Exception as e:
            print("Exception e: ",e)