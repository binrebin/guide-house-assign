import os
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# update executable_path as required

site = "mojaveofbarstove-dot-com"
uri = "https://www.mojaveofbarstow.com/used-inventory/index.htm?start="


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

def main():
    li = []
    for i in range(0, 90, 18):
        driver = Chrome(executable_path='./driver/chromedriver')
        try:            
            driver.get(f'{uri}{str(i)}')
            it = 0
            # driver.find_element_by_xpath("//button[@class='consumer-privacy-banner-button']").click()
            # target = driver.find_element(By.XPATH, '//a[text()="Please Click Here To Learn More!"]')
            # target.location_once_scrolled_into_view
            # if i == 0:
            #     
            # else:
            #     driver.execute_script("document.getElementById('inventory-results1-app-root').scrollIntoView();")
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID, "inventory-paging1-app-root")))
            driver.execute_script("document.getElementById('inventory-paging1-app-root').scrollIntoView();")
            
            

            while not page_is_loading(driver):
 
                continue
            
            soup = BeautifulSoup(driver.page_source, "lxml")
            

            # print all authors
            all_cards = soup.find_all("div", class_="vehicle-card-details-container")
            count = 0
            for crd in all_cards:
                count += 1
                
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
                li.append(data)
                data = []
            print(f"total elements {str(count)}")
            
        finally:
            # always close the browser
            driver.quit()
    write_to_file(li)

if __name__ == "__main__":
    main()
