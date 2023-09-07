import os
from time import sleep
from pandas import DataFrame
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")
#chrome_options.add_argument("--headless") # uncomment this to use chrome in headless mode
chrome_options.add_argument("window-size=1024,768")  # Open Browser in maximized mode
chrome_options.add_argument("disable-infobars")  # Disabling infobars
chrome_options.add_argument("--disable-extensions")  # Disabling extensions
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_experimental_option("prefs", {'download.default_directory': os.environ['DOWNLOAD_LOCATION']})

def download_file():
    url = 'https://player.uacdn.net/slides_pdf/DCEUPI5W006PLGL7I7MM/Process_Dynamics__Part_IV_with_anno.pdf'

    # initiate a headless chrome
    driver = webdriver.Chrome(options=chrome_options, executable_path= os.environ['CHROME_DRIVER'])
    driver.get(url)

    sleep(2)
    driver.quit()

if __name__ == "__main__":
    download_file()