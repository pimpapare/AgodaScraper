
def init():

    #------- these key are used in MainAgodaScraper file (on main agoda page)-------#

    # its used for finding next page button on main Agoda website before program can click for going to another page
    global nextPage
    nextPage = "btn.pagination2__next"

    # its used for finding accomodation id
    global accomodationIdKey
    accomodationIdKey = "data-hotelid"

    #-------------------------------------------------------------#



    #------- these key are used in SubAgodaScraper file (on each accomodation page)----------#

    # its used for finding accomodation name
    global accomodationName
    accomodationName = "hotel-header-name"

    # its used for finding accomodation address
    global accomodationAddress
    accomodationAddress = './/*[@data-selenium = "hotel-address-map"]'

    # its used for finding total review score from user
    global accomodationReviewNumber
    accomodationReviewNumber = "ReviewScore-Number"

    # its used for finding review score from user
    global accomodationReviewScore
    accomodationReviewScore = "review-basedon"

    # its used for finding useful informations that contains abount the amount of rooms/floor of each accommodotation
    global accomodationUsefulInfo
    accomodationUsefulInfo = "abouthotel-usefulinfo"

    # its used for finding facilities informations
    global accomodationFacilities  
    accomodationFacilities = "feature-group"

    # its used for finding price container
    global accomodationPriceContainer
    accomodationPriceContainer = "PriceContainer"

    # its used for finding price 
    global accomodationBestPrice
    accomodationBestPrice = "pd-price"

    global accomodationTotalPrice
    accomodationTotalPrice = "CrossedOutPrice"

    # its used for finding room type informations
    global accomodationRoomType
    accomodationRoomType = "MasterRoom__TitleName"

    # its used for finding soluout informations 
    global accomodationSoldOut
    accomodationSoldOut = "RoomGrid-searchTimeOutText"

    # its used for finding total review star
    global accomodationRateStart
    accomodationRateStart = './/*[@data-selenium = "mosaic-hotel-rating"]'

    # its used for finding lalitude
    global accomodationLatitude
    accomodationLatitude = './/*[@property = "place:location:latitude"]'

    # its used for finding longitude
    global accomodationLongitude
    accomodationLongitude = './/*[@property = "place:location:longitude"]'

    #-------------------------------------------------------------#
