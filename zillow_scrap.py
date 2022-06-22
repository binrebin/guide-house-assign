import os
import csv
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# update executable_path as required

site = "zillow-dot-com"
uris = [
    {"cat": "Sale", "url": "https://www.zillow.com/homes/"},
        {"cat": "Rent", "url": "https://www.zillow.com/homes/for_rent/"}, 
        {"cat": "Sold", "url": "https://www.zillow.com/homes/recently_sold/"}]


def page_is_loading(driver):
    while True:
        x = driver.execute_script("return document.readyState")
        if x == "complete":
            return True
        else:
            yield False


def write_to_file(list):
    print("Writing to file")
    df = pd.DataFrame(list, columns=["Category", "House Features",
                      "Address", "State", "Zip code", "Price", "Open Time/Posting Time"])
    folder = f'./scraped/{site}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = f'{folder}/{site}.csv'
    df.to_csv(filepath, encoding='utf-8',
              index=None, mode='a', header=not os.path.exists(filepath))
    print("File created !")


def main():
    
    with open('us-states.csv', mode='r') as csv_file:
        rdr = csv.DictReader(csv_file)
        for cat in uris:        
            li = []
            for row in rdr:
                driver = Chrome(executable_path='./driver/chromedriver')
                try:
                    url = cat['url']
                    categ = cat['cat']
                    print(f"Current url : {url}")
                    print(f"Row {row['Abbr']}")
                    driver.get(f'{url}')
                    driver.maximize_window()
                    driver.implicitly_wait(30)

                    it = 0
                    # driver.find_element_by_xpath("//button[@class='consumer-privacy-banner-button']").click()
                    # target = driver.find_element(By.XPATH, '//a[text()="Please Click Here To Learn More!"]')
                    # target.location_once_scrolled_into_view
                    # if i == 0:
                    #
                    # else:
                    #     driver.execute_script("document.getElementById('inventory-results1-app-root').scrollIntoView();")
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='text'])"))).send_keys(row['Abbr'])
                    # driver.execute_script(
                    #     "window.scrollTo(0,document.body.scrollHeight)")
                    # element = driver.find_element(By.TAG_NAME, "input")
                    # element.send_keys()
                    
                    # driver.execute_script(
                    #     "document.getElementById('inventory-paging1-app-root').scrollIntoView();")

                    # while not page_is_loading(driver):

                    #     continue

                    soup = BeautifulSoup(driver.page_source, "lxml")

                    # print all authors
                    all_cards = soup.find_all(
                        "div", class_="list-card-info")
                    count = 0
                    for crd in all_cards:
                        count += 1
                        hpr = [n.get_text() for n in crd.find('div', class_="list-card-heading").find_all('li')]

                        data = [
                            categ,
                            ' '.join(map(str, hpr)),
                            crd.find('address', class_='list-card-addr').get_text() if crd.find('address', class_='list-card-addr') else np.nan,
                            crd.find('address', class_='list-card-addr').get_text().split(" ")[-2] if crd.find('address', class_='list-card-addr') else np.nan,
                            crd.find('address', class_='list-card-addr').get_text().split(" ")[-1] if crd.find('address', class_='list-card-addr') else np.nan,

                            crd.find('div', class_='list-card-price').get_text() if crd.find('div', class_='list-card-price') else np.nan,

                            crd.find('div', class_='list-card-img-overlay').get_text() if crd.find('div', class_='list-card-img-overlay') else np.nan,
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
