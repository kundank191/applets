import os
from time import sleep
from pandas import read_csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import unacademy_scraper.ua_consts as ua_consts

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36")
#chrome_options.add_argument("--headless") # uncomment this to use chrome in headless mode
chrome_options.add_argument("window-size=1024,768")  # Open Browser in maximized mode
chrome_options.add_argument("disable-infobars")  # Disabling infobars
chrome_options.add_argument("--disable-extensions")  # Disabling extensions
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_experimental_option("prefs", {'download.default_directory': os.environ['DOWNLOAD_LOCATION']})

def initiate_ua_scraper():
    # initiate a headless chrome
    driver = webdriver.Chrome(options=chrome_options, executable_path= os.environ['CHROME_DRIVER'])
    driver.get(ua_consts.UA_BASE_URL)

    print('The code will pause for 30 sec, please enter otp and login till then.')
    sleep(30)

    # execute the login flow
    #login_unacademy(driver)

    # get the url list for which scraping is required
    url_list = read_csv('unacademy_scraper/ua_url_to_be_scraped.csv')['URL'].to_list()

    for url in url_list:

        driver.get(url)
        sleep(20)

        # we want to create a new folder for every url
        folder_name = driver.current_url.split('course/')[1].split('/')[0]
        new_download_dir = os.path.join(os.environ['DOWNLOAD_LOCATION'], folder_name)

        # Create the directory if it doesn't exist
        if not os.path.exists(new_download_dir):
            os.makedirs(new_download_dir)

        # Set Chrome to download files to the new directory
        driver.execute_cdp_cmd('Page.setDownloadBehavior', {'behavior': 'allow', 'downloadPath': new_download_dir})

        print(f'Download Started For : {folder_name}')

        # Find all parent elements (I'm assuming they're all wrapped in div with a specific class)
        chapter_elements = driver.find_elements(By.CSS_SELECTOR, 'div.itemContainer')

        # ok now start downloading
        for chapter_element in chapter_elements:
            
            # we will use the title to rename the pdf
            chapter_title = chapter_element.text.split('\n')[0]
            
            # check if we are able to get the SVG
            try:
                # We know that the second image is the pdf one hence the index 1
                pdf_svg = chapter_element.find_elements(By.CSS_SELECTOR, 'svg')[1]
                pdf_svg.click()

                # the element comes at parent level
                with_annotation_pdf = driver.find_element(By.XPATH, ".//p[text()='With annotation']")
                with_annotation_pdf.click()

                print(f'Chapter Downloaded : {chapter_title}')

                sleep(1)
            except:
                print(f'Chapter Download Failed : {chapter_title}')

def login_unacademy(driver):
    """
    The function will login into unacademy
    """
    login_button = driver.find_element_by_css_selector('.e13239452')
    login_button.click()
    
    # Locate the input field using the placeholder attribute, we will be using the 2nd one
    mobile_input_field = driver.find_elements_by_xpath('//input[@placeholder="Enter your mobile number"]')[1]

    # Take mobile number from user
    mobile_number = input("Enter Mobile Number : ")

    # Insert the mobile number
    mobile_input_field.send_keys(mobile_number)

    # Get OTP
    request_otp_button = driver.find_element_by_xpath('//button[text()="Login"]')
    request_otp_button.click()


    otp = input("Enter OTP : ")

    # Locate all OTP input fields using CSS selector
    otp_field = driver.find_element_by_xpath('//input[@placeholder="One time password"]')
    otp_field.send_keys(otp)