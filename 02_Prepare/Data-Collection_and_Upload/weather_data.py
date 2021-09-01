from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from user_info.user_info import driver_info


# webscrapes to retrieve specified weather station current temperature measurement
def weather_temperature():
    driver: WebDriver = webdriver.Chrome(driver_info['driver_path'])

    
    # silences almost all of the console logging done by selenium
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    
    
    driver.get(driver_info['site'])
    temperature_html = driver.find_element_by_xpath(driver_info['temp_xpath'])
    temperature = int(temperature_html.text)

    driver.quit()

    return temperature  