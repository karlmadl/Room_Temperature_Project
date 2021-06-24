from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from user_info.webdriver_location import driver_info


# webscrapes to retrieve specified weather station current temperature measurement
def weather_temperature():
    driver: WebDriver = webdriver.Chrome(driver_info['driver_path'])
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # silences almost all of the console logging done by selenium
    
    driver.get(driver_info['site'])

    temperature_html = driver.find_element_by_xpath(driver_info['xpath'])

    temperature = int(temperature_html.text)

    driver.quit()

    return temperature

