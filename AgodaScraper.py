
# AgodaScraper class is used for display program UI to user 
# It contains code part of GUI

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import dateutil.parser
from datetime import datetime
from datetime import timedelta
import datetime

import PyQt5
from PyQt5 import QtWidgets

import re

import Room
import Accommodation

import ConnectMongo
import ExportMongo
import MainAgodaScraper
import SubAgodaScraper
import GoogleCoordinates


# ---------- Functions of GUI ---------- #

def runCommand():
   
   agodaURL = getNewURL(inputAgodaURL.get())
   accommodationType = inputAccommodationType.get()
   isError = False 

   # verify agoda url
   if len(agodaURL) == 0:

      isError = True
      messagebox.showinfo("เกิดข้อผิดพลาด", "กรุณาระบุ Agoda URL")
      return

   else:

      r = re.compile('https://www.agoda.com/.*')

      if r.match(agodaURL) is None:
         isError = True
         messagebox.showinfo("เกิดข้อผิดพลาด", "กรุณาระบุ Agoda URL")
         return

   # verify specific checkIn date
   lastIndex = len(accommodationPriceList) - 1
   optionSelectedCheckIn = optionCheckInDate.get() 

   if optionSelectedCheckIn == 2:

      selectedCheckInDate = inputCheckInDate.get()
      
      r = re.compile('.*-.*-.*')

      if r.match(selectedCheckInDate) is None:
         isError = True
         messagebox.showinfo("เกิดข้อผิดพลาด", "กรุณาระบุวันในรูปแบบ ปปปป-ดด-วว\nเช่น 2000-01-01")
         return

      try:
         selectedCheckInDateCycle = int(inputCheckInDateCycle.get())
      except:
         isError = True
         messagebox.showinfo("เกิดข้อผิดพลาด", "กรุณาระบุจำนวนวันในการวนเก็บข้อมูล เช่น เก็บข้อมูลทุก 7 วัน")
         return

      if selectedCheckInDateCycle is None or selectedCheckInDateCycle == 0:
         isError = True
         messagebox.showinfo("เกิดข้อผิดพลาด", "กรุณาระบุจำนวนวันในการวนเก็บข้อมูล เช่น เก็บข้อมูลทุก 7 วัน")
         return

   else:

      selectedCheckInDateCycle = 7

      if len(accommodationPriceList) == 0:

         selectedCheckInDate = datetime.datetime.now()

      else:

         latestDate = accommodationPriceList[lastIndex]
         selectedCheckInDate = latestDate['date']
      
      selectedCheckInDate = selectedCheckInDate + timedelta(days=selectedCheckInDateCycle) 
      accommodationType = combobox.get()

   # if all infomations are complete, program will start scraping data
   if isError == False:
      startScraper(selectedCheckInDate, agodaURL, accommodationType, optionSelectedCheckIn)

def homeMenu():  
    print("homeMenu!")  

def exportMenu():  
    print("exportMenu!")  

def getNewURL(baseURL):

   splitCheckInFirst = baseURL.split('checkIn=')
   combineNewURL = baseURL

   if len(splitCheckInFirst) > 1:

      partOne = splitCheckInFirst[0]
      partTwo = splitCheckInFirst[1]
      splitPartTwo = partTwo[10: ]

      combineCheckIn = partOne + "checkIn=checkInDate" + splitPartTwo
      combineNewURL = combineCheckIn

      splitCheckOutFirst = combineCheckIn.split('checkOut=')

      if len(splitCheckOutFirst) > 1:

         partOne = splitCheckOutFirst[0]
         partTwo = splitCheckOutFirst[1]
         splitPartTwo = partTwo[10: ]
      
         combineCheckoutURL = partOne + "checkOut=checkOutDate" + splitPartTwo
         combineNewURL = combineCheckoutURL

   return combineNewURL

   
def updateList(infoArr):

   listbox.delete(0, END)

   for item in infoArr:

      try:
         dateItem = item['date']
         number = item['amount']
         dateToString = convertDateToString(dateItem)
         
         if len(dateToString) > 0:
            listbox.insert(END, " " + str(dateToString) + " : " + str(number) + " accommodations")
      except:
         listbox.insert(END, str(item))

def selectedRadio(value):
    
   optionCheckInDate = value

   if optionCheckInDate == 1:

      specificCheckInDate.delete(0, END)
      specificCheckInDate.configure(state="disabled")
      specificCheckInDate.update()

      specificLoopCheckInDate.delete(0, END)
      specificLoopCheckInDate.configure(state="disabled")
      specificLoopCheckInDate.update()
      
   else:

      specificCheckInDate.configure(state="normal")
      specificCheckInDate.update()

      specificLoopCheckInDate.configure(state="normal")
      specificLoopCheckInDate.update()
      

def getLastGoogleToken():

   try:
      googleApiKey = open("googleApiKey.txt", "r+")
      return googleApiKey.read()
   except FileNotFoundError:
      return ""

def convertDateToString(date): 

   newDateStrFormat = ""

   if type(date) is not datetime.date:
         
      try:  
         dateTimeObj = dateutil.parser.parse(str(date))
         newDateStrFormat = dateTimeObj.strftime("%Y-%m-%d")

      except:
         newDateStrFormat = ""
         print("ERROR: " + str(date))

   else: 

      newDateStrFormat = date

   return newDateStrFormat

def exportAccommodationsDataToExcelFile():

   dateAndTime = datetime.datetime.now()
   today = dateAndTime.strftime("%d_%m_%Y ")

   export = ExportMongo.Exporter()
   export.exportAccommodationObjectsFromMongoToCSV(today)

def exportRoomPriceDataToExcelFile():

   dateAndTime = datetime.datetime.now()
   today = dateAndTime.strftime("%d_%m_%Y ")

   export = ExportMongo.Exporter()
   export.exportRoomObjectsFromMongoToCSV(today)

def exportRoomPriceWithOutREplacingInfoDataToExcelFile():

   dateAndTime = datetime.datetime.now()
   today = dateAndTime.strftime("%d_%m_%Y ")

   export = ExportMongo.Exporter()
   export.exportRoomWithoutReplacingInfoObjectsFromMongoToCSV(today)


def saveGoogleApiKey():

   googleAPIKey = inputGoogleApiKey.get()

   try:
      googleApiKey = open("googleApiKey.txt", "r+").read()
      googleApiKey = googleApiKey.replace(googleApiKey,googleAPIKey)
      
      googleFile = open("googleApiKey.txt", 'w')
      googleFile.write(googleApiKey)
      googleFile.close()

   except FileNotFoundError:
      
      googleApiKey = open("googleApiKey.txt", "r+")
      googleApiKey.write(googleAPIKey)
      googleApiKey.close()

# ---------- End Functions of GUI ---------- #



# ---------- Functions For Scraping Data Part ---------- #

# this function is used for scraping accommodation id from main page of Agoda web site
def startScraper(checkInDate, baseAgodaURL, agodaType, optionType):

   # verify type of checkIn date: if it isn't date time type -> convert it to date time before using
   if type(checkInDate) is not datetime.date:

      try:  
         newCheckInDateDateFormat = dateutil.parser.parse(str(checkInDate))
      except:
         newCheckInDateDateFormat = checkInDate

   else:
         newCheckInDateDateFormat = checkInDate

   if optionType == 2:
      checkInDate = newCheckInDateDateFormat
   else:
      # start scraping data only on Monday
      startOfWeek = newCheckInDateDateFormat - timedelta(days=newCheckInDateDateFormat.weekday())  
      # endOfWeek = startOfWeek + timedelta(days=7)  # Monday
      # Get first date of week
      checkInDate = startOfWeek

   # it will loop until user close the program
   while True:

      # set checkOut date greater than checkIn date
      checkOutDate = checkInDate + timedelta(days=1)

      # convert checkInDate and checkOutDate to string type
      checkInDateString = checkInDate.strftime("%Y-%m-%d")
      checkOutDateString = checkOutDate.strftime("%Y-%m-%d")

      # replace checkInDate and checkOutDate string to agoda base url
      replaceCheckin = baseAgodaURL.replace('checkInDate',checkInDateString)
      replaceCheckOut = replaceCheckin.replace('checkOutDate',checkOutDateString)

      agodaUrl = replaceCheckOut

      # start scrape accommodation informations from Agoda website
      scraper = MainAgodaScraper.MainAgodaScraper(agodaUrl)
      scraper.getURL()
      scraper.loadAgodaUrl()
    
      try:

         # get total page that available on Agoda 
         page = scraper.driver.find_element_by_class_name("pagination2__text")
         totalPageNumber = page.text.split("of ", 2)

         # loop until reaching last page
         for i in range(int(totalPageNumber[1]) - 1):

            # program will scrape all informations from MainAgodaScraper.py
            scraper.extractInformations(checkInDate, googleAPIKey, accommodationType)

            # if program finished to scrape all informations then it will go to next page and continue scraping
            try:

               nextURL = scraper.loadUrlNextPage()
               
               if len(nextURL) > 0:
                  scraper.loadAgodaUrl()
               else:
                  continue

            except Exception as e:
               print("Exception start scraping: ", e)

      except Exception as e:
        print("Exception start scraping loop: ",e)

      try:
         checkInDate = checkInDate + timedelta(days=int(selectedCheckInDateCycle)) 
      except:
         checkInDate = checkInDate + timedelta(days=7)


# this function is used for adjusting checkIn and checkOut data
def getCheckInAndCheckOutDate(startDate):

   checkInDateString = startDate.strftime("%Y-%m-%d")
   checkInDate = dateutil.parser.parse(str(checkInDateString))

   checkOutDate = startDate + timedelta(days=1)
   checkOutDateString = checkOutDate.strftime("%Y-%m-%d")

   return {'checkInDate': checkInDate, 'checkOutDate': checkOutDate, 'checkInDateString': checkInDateString, 'checkOutDateString': checkOutDateString}

# ---------- End Functions For Scraping Data Part ---------- #




# ---------- GUI Part ---------- #

# retreive data from DB
db = ConnectMongo.Connector()

accommodationPriceList = db.getAmountsOfAccommodationInEachDate()
allAccommodationList = db.getAllAccommodationObjects()

# initial UI frame
root = Tk()
root.geometry("600x570")
root.title("Agoda Scraper")

frame = Frame(root)
frame.pack()

var = StringVar()

optionCheckInDate = IntVar()
optionCheckInDate.set(1)

optionSelectedCheckIn = IntVar()

inputCheckInDate = StringVar()
inputCheckInDateCycle= StringVar()
inputCheckInDateCycle.set("7")

selectedCheckInDateCycle = IntVar()
selectedCheckInDateCycle.set(7)

inputAgodaURL = StringVar()
inputGoogleApiKey = StringVar()
inputAccommodationType = StringVar()

# set room type = hotel by default
inputAccommodationType.set("hotel")

agodaURL = str()
googleAPIKey = str()
accommodationType = str()
accommodationType = "hotel"

frameTitle = Frame()
frameTitle.pack(fill="x", padx=18)
Label(frameTitle, text= '{}{}{}'.format('ข้อมูลปัจจุบันในระบบของโรงแรม ', allAccommodationList.count(), ' แห่ง ในจังหวัดเชียงใหม่'), highlightbackground= 'black').pack(side="left", pady = 10)

frameSubTitle = Frame()
frameSubTitle.pack(fill="x", padx=18)
Label(frameSubTitle, text= "จำแนกโดย วันที่เข้าพัก : จำนวนโรงแรม", highlightbackground= 'black').pack(side = "left")

frameGroupOne = Frame()
frameGroupOne.pack(padx = 20)

listbox = Listbox(frameGroupOne, width=60, height=8)
listbox.pack(side="left", fill="both",expand=True, ipady= 10)

scrollbar = Scrollbar(frameGroupOne, orient="vertical")
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")

listbox.config(yscrollcommand=scrollbar.set)

updateList(accommodationPriceList)

frameGroupConfigTitle = Frame()
frameGroupConfigTitle.pack()

frameSetting = Frame()
frameSetting.pack(fill="x", padx=20, pady=20)

labelSettingframe = LabelFrame(frameSetting, text="ตั้งค่าโปรแกรม")
labelSettingframe.pack(fill="x", ipady = 5)

Label(labelSettingframe, text="Agoda URL:").grid(row=1,column=0, sticky = "e")
specificBaseURL = Entry(labelSettingframe, textvariable=inputAgodaURL)
specificBaseURL.grid(row=1,column=1)

Label(labelSettingframe, text="Google Api key:").grid(row=2,column=0, sticky = "e")
specificGoogleAPiKey = Entry(labelSettingframe, textvariable=inputGoogleApiKey)
specificGoogleAPiKey.grid(row=2,column=1)
Button(labelSettingframe, text="บันทึก", command=saveGoogleApiKey).grid(row=2,column=2,pady=10, ipady=2, ipadx=5, padx=5, sticky = "w")

existingGoogleKey = getLastGoogleToken()

if len(existingGoogleKey) > 0:
   specificGoogleAPiKey.insert(0, str(existingGoogleKey))

# google token
Label(labelSettingframe, text="ประเภทของที่พัก:").grid(row=3,column=0, sticky = "e")

combostyle = ttk.Style()

combostyle.theme_create('combostyle',
                         settings = {'TCombobox':
                                     {'configure':
                                      {
                                       'background': 'white'
                                       }}}
                         )
combostyle.theme_use('combostyle') 

combobox = ttk.Combobox(labelSettingframe, values=["hotel"])
combobox.current(0)
combobox.grid(row=3,column=1)

Label(labelSettingframe, text="ช่วงเวลาการเก็บข้อมูล").grid(row=4,column=0, sticky = "w", ipady = 10)

Radiobutton(labelSettingframe, text='เก็บข้อมูลทุกต้นสัปดาห์', variable=optionCheckInDate, value=1, command=lambda : selectedRadio(1)).grid(row=5,column=0,padx = 20, sticky ="w")
Radiobutton(labelSettingframe, text='เก็บข้อมูลโดยการระบุวัน ', variable=optionCheckInDate, value=2, command=lambda : selectedRadio(2)).grid(row=6,column=0,padx = 20, sticky ="w")

specificCheckInDate = Entry(labelSettingframe, textvariable=inputCheckInDate, state = "disabled")
specificCheckInDate.grid(row=6,column=1)
Label(labelSettingframe, text="ตัวอย่าง 2000-01-01", font=(18)).grid(row=6,column=2, sticky = "w")

Label(labelSettingframe, text="ระยะเวลาในการวนเก็บข้อมูล/วัน").grid(row=7,column=0, sticky = "e")
specificLoopCheckInDate = Entry(labelSettingframe, textvariable=inputCheckInDateCycle, state = "disabled")
specificLoopCheckInDate.grid(row=7,column=1)

frameBtn = Frame()
frameBtn.pack()
# Button(frameBtn, text="นำออกข้อมูลโรงแรม", command=exportAccommodationsDataToExcelFile).grid(row=8,column=0,ipady=5,ipadx=15)
# Button(frameBtn, text="นำออกข้อมูลราคาโรงแรม", command=exportRoomPriceDataToExcelFile).grid(row=8,column=1,padx=10,ipady=5,ipadx=15)
Button(frameBtn, text="เริ่มเก็บข้อมูล", command=runCommand).grid(row=8,column=3,ipady=5,ipadx=15)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="นำออกข้อมูลที่พัก", command=exportAccommodationsDataToExcelFile)
filemenu.add_command(label="นำออกข้อมูลราคาที่พักแบบมีการอัพเดทข้อมูล", command=exportRoomPriceDataToExcelFile)
filemenu.add_command(label="นำออกข้อมูลราคาที่พักทั้งหมด", command=exportRoomPriceWithOutREplacingInfoDataToExcelFile)
filemenu.add_separator()
menubar.add_cascade(label="นำออกข้อมูล", menu=filemenu)

root.config(menu=menubar)


root.mainloop()

# ---------- End of GUI Part---------- #
