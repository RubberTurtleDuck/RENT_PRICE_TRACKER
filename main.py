from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pprint import pprint

PROPERTIES_PAGE = ("https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&"
                   "minBedrooms=1&maxPrice=1000&minPrice=300&propertyTypes=&includeLetAgreed=false&mustHave=&"
                   "dontShow=&furnishTypes=&keywords=")
GOOGLE_FORM_LINK = "https://forms.gle/qGf1dKVG7kD5rP3D7"
CHROME_DRIVER_PATH = "/Users/Mr.Coffeeman/Development/chromedriver"

main_page = requests.get(PROPERTIES_PAGE)
soup = BeautifulSoup(main_page.text, "html.parser")

all_properties = soup.find_all(name="div", class_="l-searchResult")

address_list = soup.find_all(name="address", class_="propertyCard-address")
addresses = [address.text.strip("\n") for address in address_list]


price_list = soup.find_all(name="span", class_="propertyCard-priceValue")
prices = [price.text for price in price_list]

all_property_links = soup.find_all(name="a", class_="propertyCard-priceLink")
links = [link.get("href") for link in all_property_links if all_property_links.index(link) % 2 == 0]

driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
driver.get(GOOGLE_FORM_LINK)
time.sleep(5.0)

for i in range(len(addresses)):
    q1 = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/"
                                       "div/div[1]/input")
    q1.send_keys(addresses[i])

    q2 = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/"
                                       "div/div[1]/input")
    q2.send_keys(prices[i])

    q3 = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/"
                                       "div/div[1]/input")
    q3.send_keys(f"https://www.rightmove.co.uk{links[i]}")

    submit_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div")
    submit_button.click()

    if i <= len(addresses):
        restart = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
        restart.click()
        time.sleep(1.0)
    else:
        break

