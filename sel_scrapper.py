import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

uri = "https://www.mojaveofbarstow.com/used-inventory/index.htm?start="

pg_list = []
site = "mojaveofbarstove-dot-com"

print(f"Scrapping started.")


def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False


def write_to_file(list):
    print("Writing to file")
    df = pd.DataFrame(list, columns =["Title", "Model", "Year", "Engine Specification", "Wheel Specification", "Price", "Stock #", "interior color", "exterior color", "miles"])
    folder = f'./scraped/{site}'
    if not os.path.exists(folder):
        os.makedirs(folder)

    df.to_csv (f'{folder}/{site}.csv', encoding='utf-8', index = None, header=True)
    print("File created !")

def load_driver(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')

    # options.headless = True
    service_obj = Service("./driver/chromedriver")
    driver = webdriver.Chrome(service=service_obj)
    try:
        print(f"Trying to load page: {url}")
        driver.get(url)
        return driver
    except WebDriverException:
        return None

def main():
    for i in range(0, 90, 18):
        driver = load_driver(f'{uri}{str(i)}')
        it = 0
        if not driver:
            print("Page down")
            if len(pg_list) != 0:
                write_to_file(pg_list)
        else:
            print("Waiting for page to load")
            while not page_is_loading(driver):
                continue

            # time.sleep(10)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            print("Souped!")
            all_cards = soup.find_all('div', class_= 'vehicle-card-details-container')
            
            for crd in all_cards:
                it += 1
                data = [
                    crd.find('a').get_text() if crd.find('a') else np.nan,
                    crd.find('span', class_='ddc-font-size-small').get_text() if crd.find('span', class_='ddc-font-size-small') else np.nan,
                    crd.find('a').get_text().split(" ")[0] if crd.find('a') else np.nan,
                    crd.find('li', class_='engine').get_text() if crd.find('li', class_='engine') else np.nan,
                    crd.find('li', class_='driveLine').get_text() if crd.find('li', class_='driveLine') else np.nan,
                    crd.find('span', class_='portal-price').get_text() if crd.find('span', class_='portal-price') else np.nan,
                    crd.find('li', class_="stockNumber").get_text().split(":")[-1] if crd.find('li', class_="stockNumber") else np.nan,
                    crd.find('li', class_="interiorColor").get_text() if crd.find('li', class_="interiorColor") else np.nan,
                    crd.find('li', class_="exteriorColor").get_text() if crd.find('li', class_="exteriorColor") else np.nan,
                    crd.find('li', class_="odometer").get_text() if crd.find('li', class_="odometer") else np.nan
                ]
                if len(data) == 0:
                    print("No data for iteration: {it}")
                else:
                    pg_list.append(data)
            print("Doc collected for page: {it}")

    print(f"Total docs collected: {str(len(pg_list))}")
    write_to_file(pg_list)
    print(f"Chrome driver shutting down")
    driver.close()
    print(f"Finished !")


if __name__ == "__main__":
    main()
