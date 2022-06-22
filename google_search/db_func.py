import csv
import os
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import tkinter.messagebox
import requests
import re
import time
import random
import decimal
import json
import argparse
from urllib.parse import urlparse
from fake_useragent import UserAgent
import numpy as np



def write_to_file(list, query):
    print("Writing to file")
    df = pd.DataFrame(list, columns=["URL", "Tile", "Text"])
    folder = f'./data'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = '-'.join(query.split(' '))
    filepath = f'{folder}/{filename}.csv'
    df.to_csv(filepath, encoding='utf-8', index_label="Id", mode='a', header=not os.path.exists(filepath))
    print("File created !")



def insert(query, start):
    results = []

    referrer = 'https://www.github.com/'
    page = 1
    startnum = 0

    query = query.replace(' ', '+')
    session = requests.session()
    response = session.get('https://google.com')
    cookies = session.cookies.get_dict()

    # set default headers
    headers = {'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': referrer,
                'Upgrade-Insecure-Requests': '1'
                }
    # add cookies to headers
    for k, v in cookies.items():
        headers[k] = v

    # construct url
    url = 'https://www.google.com/search?q=' + query


    url = url + '&num=100' '&start=' + str(start)

    resp = requests.get(url, headers=headers, verify=False)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "lxml")

        regex = re.compile(r"^(?=.*:)[^:]*")

        all_cards = soup.find_all('div', class_="g")
        for g in all_cards:
            url = g.find("div", {"data-header-feature" : "0"}).find('a')['href'] if g.find("div", {"data-header-feature" : "0"}) else np.nan
            title = g.find("div", {"data-header-feature" : "0"}).find('h3').get_text() if g.find("div", {"data-header-feature" : "0"}) else np.nan
            text = g.find("div", {"data-content-feature" : "1"}).find('div').get_text() if g.find("div", {"data-content-feature" : "1"}) else np.nan
            print(f'Title : {title}')
            results.append([url, title, text])
        write_to_file(results, query)


def view():
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    cur_obj.execute("SELECT * FROM book")
    rows = cur_obj.fetchall()
    conn_obj.close()
    return rows


def delete(id):
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    cur_obj.execute("DELETE FROM book "
                    "WHERE id = ?", (id,))
    conn_obj.commit()
    conn_obj.close()


def insert_csv(filename):
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    with open(filename, 'r') as fin:
        dr = csv.DictReader(fin)
        Cols = dr.fieldnames
        numCols = len(Cols)
        to_db = [tuple(i.values()) for i in dr]
        ColString = ','.join(Cols)

        QuestionMarks = ["?"] * numCols
        ToAdd = ','.join(QuestionMarks)
        cur_obj.executemany(
            f"INSERT INTO book ({ColString}) VALUES ({ToAdd});", to_db)
    conn_obj.commit()
    conn_obj.close()


def download_csv():
    conn_obj = sqlite3.connect("addressbook.db")
    db_df = pd.read_sql_query("SELECT * FROM book", conn_obj)
    filename = 'database.csv'
    db_df.to_csv(filename, index=False)
    tkinter.messagebox.showinfo("Download Complete",  "download.csv saved !")
    
