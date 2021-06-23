from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

PATH = "C:\Program Files (x86)\chromedriver.exe"
WEBSITE = "https://www.wunderground.com/weather/us/nj/howell-township/KNJHOWEL37"
XPATH = "/html/body/app-root/app-today/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div/div[2]/div/div/div[2]/lib-display-unit/span/span[1]"


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

