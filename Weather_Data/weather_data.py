from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

PATH = "CHROMEDRIVER.EXE PATH"
WEBSITE = "WEATHER STATION REPORTING WEBSITE"
XPATH = "XPATH OF HTML ELEMENT INCLUDING TEMPERATURE TEXT"


# webscrapes to retrieve specified weather station current temperature measurement
def weather_temperature():
    driver: WebDriver = webdriver.Chrome(PATH)
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # silences almost all of the console logging done by selenium
    
    driver.get(WEBSITE)

    temperature_html = driver.find_element_by_xpath(XPATH)

    temperature = int(temperature_html.text)

    driver.quit()

    return temperature

