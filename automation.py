from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime
from pathlib import Path
from selenium.webdriver.common.action_chains import ActionChains
import pytz
import time

def setup_date(driver, selectors,days_to_add=7):
    
            # List of selector types to try
        selectors_type = [By.XPATH, By.CSS_SELECTOR]

        # Define days to add for the return date
        days_to_add = 7  # Example: return date is 7 days from "today"

        # Set the timezone to New Zealand
        nz_timezone = pytz.timezone('Pacific/Auckland')
        now = datetime.now(nz_timezone)  # Current date and time in New Zealand


        # Check if the current time is after 22:00; if so, set "today" to the next day
        if now.hour >= 22:
            today = now + timedelta(days=1)
        else:
            today = now

        # Calculate the return date by adding days_to_add
        return_date = today + timedelta(days=days_to_add)

        # Format dates as strings
        today_str = today.strftime('%Y-%m-%d')
        return_date_str = return_date.strftime('%Y-%m-%d')

        # Define potential XPATH variants based on selector CSS
        selector_variants_today = [
            {"by": By.XPATH, "selector": f"//button[@date='{today_str}']"},
            {"by": By.XPATH, "selector": f"//button[text()='{today.day}']"},
            {"by": By.XPATH, "selector": f"//td[@class='today start selected']"},
            {"by": By.XPATH, "selector": f"//a[@class='ui-state-default'][text()='{today.day}']"},
            {"by": By.XPATH, "selector": f"//td[@data-month='{today.month - 1}'][@data-year='{today.year}']/a[text()='{today.day}']"}
        ]
        selector_variants_return = [
            {"by": By.XPATH, "selector": f"//button[@date='{return_date_str}']"},
            {"by": By.XPATH, "selector": f"//button[text()='{return_date.day}']"},
            {"by": By.XPATH, "selector": f"//a[@class='ui-state-default'][text()='{return_date.day}']"},
            {"by": By.XPATH, "selector": f"//td[@data-month='{return_date.month - 1}'][@data-year='{return_date.year}']/a[text()='{return_date.day}']"}
        ]
        
        
    
        # List of selector types to try
        #selectors_type = [By.XPATH, By.CSS_SELECTOR]
        
        # Try each selector type until one works
        for selector_type in selectors_type:
            try:
                Pick_up_date_banner = driver.find_element(selector_type, selectors['pickup_calendar'])
                Pick_up_date_banner.click()
                print("Pick-up date banner selected")
                
                for variant in selector_variants_today:
                    try:
                        date_element = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((variant["by"], variant["selector"]))
                        )
                        date_element.click()
                        
                        print("Today's date selected successfully.")
                        break
                    except Exception as e:
                        print(f"Pickup date selection failed with error: {e}")
                    
                break  # Exit loop if element is found and clicked
            except Exception as e:
                print(f"Pick-up date failed with error: {e}")
                continue  # Try next selector type if current one fails
        
                # Try each selector type until one works
        for selector_type in selectors_type:
            try:
                return_date_banner = driver.find_element(selector_type, selectors['return_calendar'])
                return_date_banner.click()
                print("return date banner selected")
                
                for variant in selector_variants_return:
                    try:
                        date_element = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((variant["by"], variant["selector"]))
                        )
                        date_element.click()
                        
                        print("return date setted successfully.")
                        break
                    except Exception as e:
                        print(f"return  date setting failed with error: {e}")
                    continue  # Try next selector type if current one fails
                    
                break  # Exit loop if element is found and clicked
            except Exception as e:
                print(f"return  date failed with error: {e}")
                continue  # Try next selector type if current one fails
        
    
def setup_time(driver, selectors):
    
        # Set the timezone to New Zealand
        nz_timezone = pytz.timezone('Pacific/Auckland')
        now = datetime.now(nz_timezone)
        hour = now.hour
        minute = now.minute

        # Round the minutes to the nearest half-hour
        current_hour = hour
        current_minute = "30" if minute >= 30 else "00"

        # Adjust time based on the 8:00 to 22:00 range
        if hour < 8:
            # Before 8:00, set to 8:00
            current_hour = "08"
            current_minute = "00"
        elif hour >= 22:
            # After 22:00, set to 8:00 of the next day
            current_hour = "08"
            current_minute = "00"
        else:
            # Convert hour to two-digit string for consistency
            current_hour = f"{current_hour:02d}"

        current_time_str = f"{current_hour}:{current_minute}"
        current_time_value = f"{current_hour}{current_minute}"
        return_time="22:00"
    
        # List of selector types to try
        selectors_type = [By.XPATH, By.CSS_SELECTOR]

        # Try each selector type until one works
        for selector_type in selectors_type:
            try:
                time.sleep(10)
                Pick_up_time_banner = driver.find_element(selector_type, selectors['pickup_time_input_click'])
                Pick_up_time_banner.click()
                
                print("Pick-up time banner selected")
                

                try: 
                        # Attendre que les éléments de temps soient chargés
                        time_elements = WebDriverWait(driver, 2).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "time-picker__timevalue"))
                        )

                        # Rechercher et faire défiler jusqu'à l'heure choisie
                        for element in time_elements:
                            time_text = element.find_element(By.TAG_NAME, "span").text
                            if time_text == current_time_str:
                                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
                                time.sleep(5) 
                                # Attendre pour s'assurer que le défilement est terminé et clické
                                driver.execute_script("arguments[0].click();", element)
                                break
                        else:
                            print("Heure non trouvée dans la liste.")
    
                except Exception as e:
                    print(f"le scrolle na pas marcher parce que {e}")

                break  # Exit loop if element is found and clicked
            except Exception as e:
                print(f"Pick-up time banner failed with error: {e}")
                continue  # Try next selector type if current one fails
               
            
        # Try each selector type until one works
        for selector_type in selectors_type:
            try:
                return_time_banner = driver.find_element(selector_type, selectors['return_time_input_click'])
                return_time_banner.click()
                print("return time banner selected")
                
                try: 
                        # Attendre que les éléments de temps soient chargés
                        time_elements = WebDriverWait(driver, 2).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "time-picker__timevalue"))
                        )

                        # Rechercher et faire défiler jusqu'à l'heure choisie
                        for element in time_elements:
                            time_text = element.find_element(By.TAG_NAME, "span").text
                            if time_text == return_time:
                                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
                                time.sleep(5) 
                                # Attendre pour s'assurer que le défilement est terminé et clické
                                driver.execute_script("arguments[0].click();", element)
                                break
                        else:
                            print("Heure non trouvée dans la liste.")
                            
                except Exception as e:
                    print(f"le scrolle na pas marcher parce que {e}")    
                                                
                continue  # Try next selector type if current one fails
                    
                break  # Exit loop if element is found and clicked
            
            except Exception as e:
                print(f"return time failed with error: {e}")
                continue  # Try next selector type if current one fails
    
    
def setup_location(driver, selectors):
        
        # List of selector types to try
        selectors_type = [By.XPATH, By.CSS_SELECTOR]

        # Try each selector type until one works
        for selector_type in selectors_type:
            try:
                location_input_box = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['location_input']))
                )
                location_input_box.send_keys("Auckland Airpo")
                location_input_box.send_keys(Keys.RETURN)
                
                print("clicked on location field")
             
                try:
                    for selector_type in selectors_type:
                        
                # Select the first suggestion for the location
                        select_first_suggestion = WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, selectors['location_suggestion']))
                        )
                        select_first_suggestion.click()
                        print("Pick-up location set")
                        
                        break 
                except Exception as e:
                    print(f"Pick-up location selecting suggestion failed with error: {e}")
                    continue  # Try next selector type if current one fails
                    
                break  # Exit loop if element is found and clicked
            except Exception as e:
                print(f"Pick-up location setting failed with error: {e}")
                continue  # Try next selector type if current one fails
               
    
def search_button( driver, selectors):
        # List of selector types to try
        selectors_type = [By.XPATH, By.CSS_SELECTOR]
        
        for selector_type in selectors_type:
            try:
                search_button= WebDriverWait(driver,3).until(EC.element_to_be_clickable((selector_type, selectors["search_button"]))).click()
            except Exception as e : 
                print(f"Search button setting failed with error: {e}")
        
        
def select_country(driver, selectors):
    pass
        
    
def next_page(self, selector):
        pass
    
    
def fill_form(driver, selectors):
        try:
            # Set up the pick-up location
            setup_location(driver, selectors)
            #time.sleep(30)
            
            
            # Set up the pick-up and return dates
            setup_date(driver, selectors, days_to_add=7)
            
            
            # Set up the pick-up and return times
            setup_time(driver, selectors)
            time.sleep(2)
            
            # Click the search button to submit the form
            search_button(driver, selectors)
            time.sleep(10)
            
            print("Form filled and submitted successfully.")
        except (TimeoutException, NoSuchElementException) as e:
            print(f"An error occurred while filling the form: {e}")
        
        pass
    


        
        
        
        
        
        
        
        
        