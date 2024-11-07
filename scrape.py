import undetected_chromedriver as uc  # Use undetected-chromedriver
import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from workflow_dict import workflow_dict
from automation import fill_form

load_dotenv()
   
# Scraping and parsing utilities
def scrape_website(base_url):
    """
    Scrape content from all pages, including paginated results, into a single large HTML file.
    """
    options = uc.ChromeOptions()
    options.headless = False  # Change to False if you want to see the browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--enable-javascript")
  

    giant_html = ""  # This will store all the HTML from the pages

    driver = None
    
    try:
        # Initialize the browser
        driver = uc.Chrome(driver_executable_path=r"chromedriver-win64\chromedriver.exe", options=options)
        
        # Visit the first page
        driver.get(base_url)
        time.sleep(5)  # Wait for the page to load the page 
        
        #fill_form(driver,workflow_dict["f'{base_url}"])
        fill_form(driver, workflow_dict[base_url])

        # Add the HTML of the first page to the giant HTML string
        giant_html += driver.page_source
        
        # Keep track of the previous page's source to detect when pagination ends
        previous_page_source = driver.page_source
        
        # Check for pagination and scrape subsequent pages
        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Try to find the "next page" button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, '#center-container > div.ResultsView_ResultsView__MGMyM > nav > div:nth-child(3) > button > span:nth-child(1) > svg')
                
                # Check if the button is enabled or if the page content does not change
                if next_button.is_enabled():
                    next_button.click()  # Click the next button
                    time.sleep(5)  # Wait for the next page to load
                    
                    # Check if the page source has changed after clicking "Next"
                    current_page_source = driver.page_source
                    if current_page_source == previous_page_source:
                        print("No more pages to scrape.")
                        break
                        
                    # Update previous page source for the next iteration
                    previous_page_source = current_page_source
                    
                    # Add the HTML of the next page to the giant HTML
                    giant_html += current_page_source
                else:
                    # The "Next" button is disabled, stop scraping
                    print("Next button is disabled or no more pages to scrape.")
                    break
            except Exception as e:
                print(f"An error occurred while paginating: {str(e)}")
                break

        # Return all the collected HTML
        return giant_html

    except Exception as e:
        print(f"An error occurred during scraping: {str(e)}")
        return ""

    finally:
        # Ensure the browser is always closed
        if driver is not None:
            driver.quit()
            print("Browser closed.")


def extract_body_content(html_content):
    """
    Extracts all the <body> content from the concatenated HTML of multiple pages.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <body> tags in the giant HTML
    body_contents = soup.find_all("body")
    
    # Combine all body contents into a single string
    combined_body_content = ""
    for body in body_contents:
        combined_body_content += str(body)  # Convert each <body> to string and append

    return combined_body_content


def clean_body_content(body_content):
    """
    Cleans the extracted body content by removing unwanted elements like scripts and styles.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()  # Remove scripts and styles

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=20000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
