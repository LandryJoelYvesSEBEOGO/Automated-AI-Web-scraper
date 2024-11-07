from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

today = datetime.today().strftime('%Y-%m-%d')  # Format : AAAA-MM-JJ
# Get the current time and round minutes to the nearest half-hour (00 or 30)
now = datetime.now()
current_hour = now.strftime("%H")
current_minute = "30" if now.minute >= 30 else "00"
current_time_str = f"{current_hour}:{current_minute}"
current_time_value = f"{current_hour}{current_minute}"


Avis = {
}


Europcar = {
    'pickup_time_input_click': "//*[@id='hero-booking-pod-id']/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div",
    'return_time_input_click': "//*[@id='hero-booking-pod-id']/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/input",
    'location_input': "#location-search-pickup > div > div.location-search-autocomplete__input-container > div > div > div.ecw-input__text-line > input",
    'location_suggestion': "#location-search-pickup > div > div.location-search-autocomplete__suggestions.location-search-autocomplete__suggestions--is-desktop-view > div > div > div:nth-child(1) > div:nth-child(2) > div > span",
    'pickup_calendar': "#datepicker-pickup",
    'return_calendar': "#datepicker-dropoff",
    'search_button': "#hero-booking-pod-id > div > div > div.ecw-booking-pod__bottom-container > button",
}

Budget = {}

Hertz = {}
Thrifty = {}
Ezi_Car_Rental = {}
Omega_Rental_Cars = {}
Go_Rentals = {}
Apex_Car_Rentals = {}
Snap_Rentals = {}
Lucky_Rentals = {}
Drive_NZ_Rentals = {}
NZ_Rent_A_Car = {}
Ace_Rental_Cars = {}
Abell_Car_Rentals = {}
Scottsdale_Car_Hire = {}
Action_Rentals = {}
Christchurch_Car_Hire = {}
Escape_Rentals = {}
Maui_Motorhomes = {}
Mighway = {}
Tiki_Touring_Rentals = {}
New_Zealand_Cars_Rental = {}
Airport_Rentals = {}
Jucy_Rentals = {}
Enterprise_Rent_A_Car = {}
Rental_Cars_NZ = {}
Kiwi_Direct_Car_Rentals = {}
USave_Car_Truck_Rentals = {}
RaD_Car_Hire = {}
Yes_Rentals_NZ = {}
Touchdown_Car_Rentals = {}
Big_Value_Car_Rentals = {}
Discount_Car_Rental_NZ = {}
Auto_Europe = {}
Economy_Car_Rentals = {}
DriveNow = {}
Sixt_New_Zealand = {}
EZU_Car_Rental = {}
GO_Cheap_Car_Rentals = {}
Booking_com = {}
Skyscanner = {}

workflow_dict = {
    "https://www.avis.co.nz/en/home": Avis,
    "https://www.budget.co.nz": Budget,
    "https://www.europcar.co.nz": Europcar,
    "https://www.hertz.co.nz": Hertz,
    "https://www.thrifty.co.nz": Thrifty,
    "https://www.ezicarrental.co.nz": Ezi_Car_Rental,
    "https://www.omegarentalcars.com": Omega_Rental_Cars,
    "https://www.gorentals.co.nz": Go_Rentals,
    "https://www.apexrentals.co.nz": Apex_Car_Rentals,
    "https://www.snaprentals.co.nz": Snap_Rentals,
    "https://www.luckyrentals.co.nz": Lucky_Rentals,
    "https://www.drivenz.co.nz": Drive_NZ_Rentals,
    "https://www.nzrentacar.co.nz": NZ_Rent_A_Car,
    "https://www.acerentalcars.co.nz": Ace_Rental_Cars,
    "https://www.abell.co.nz": Abell_Car_Rentals,
    "https://www.scottsdalecars.co.nz": Scottsdale_Car_Hire,
    "https://www.actionrentals.co.nz": Action_Rentals,
    "https://www.christchurchcarhire.co.nz": Christchurch_Car_Hire,
    "https://www.escaperentals.co.nz": Escape_Rentals,
    "https://www.maui.co.nz": Maui_Motorhomes,
    "https://www.mighway.com": Mighway,
    "https://www.tikitouring.co.nz": Tiki_Touring_Rentals,
    "https://www.newzealandcarsrental.com": New_Zealand_Cars_Rental,
    "https://www.airportrentals.com": Airport_Rentals,
    "https://www.jucy.com": Jucy_Rentals,
    "https://www.enterprise.co.nz": Enterprise_Rent_A_Car,
    "https://www.rentalcars.com": Rental_Cars_NZ,
    "https://www.kiwirentalcars.co.nz/#/searchcars": Kiwi_Direct_Car_Rentals,
    "https://www.usave.co.nz": USave_Car_Truck_Rentals,
    "https://www.radcarhire.co.nz": RaD_Car_Hire,
    "https://www.yesrentals.co.nz": Yes_Rentals_NZ,
    "https://www.touchdowncarrental.co.nz": Touchdown_Car_Rentals,
    "https://www.bigvalue.co.nz": Big_Value_Car_Rentals,
    "https://www.discountcarrental.co.nz": Discount_Car_Rental_NZ,
    "https://www.autoeurope.com": Auto_Europe,
    "https://www.drivenzrental.co.nz": Drive_NZ_Rentals,
    "https://www.economycarrentals.com": Economy_Car_Rentals,
    "https://www.drivenow.com.au": DriveNow,
    "https://www.sixt.nz": Sixt_New_Zealand,
    "https://www.ezu.com.nz": EZU_Car_Rental,
    "https://www.gocheap.co.nz": GO_Cheap_Car_Rentals,
    "https://www.booking.com": Booking_com,
    "https://www.skyscanner.co.nz": Skyscanner
}

