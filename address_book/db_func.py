import sqlite3
import csv
import pandas as pd
import tkinter.messagebox


def connect():
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    cur_obj.execute("CREATE TABLE IF NOT EXISTS "
                    "book (id integer PRIMARY KEY, "
                    "fname text, "
                    "mname text, "
                    "lname text, "
                    "age integer, "
                    "addr_1 text, "
                    "city text,"
                    "state text,"
                    "ph_num text)")
    conn_obj.commit()
    conn_obj.close()


def insert(fname, mname, lname, age, addr_1, city, state, ph_num):
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    cur_obj.execute("INSERT INTO book "
                    "VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)", (fname, mname, lname, age, addr_1, city, state, ph_num))
    conn_obj.commit()
    conn_obj.close()


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


def download_csv(age_min, age_max):
    age_max = int(age_max) if age_max != '' else 0
    age_min = int(age_min) if age_min != '' else 0
    print(f'agemin-{age_min}-{type(age_min)} : agemax-{age_max}-{type(age_max)}')
    conn_obj = sqlite3.connect("addressbook.db")
    if age_min == 0 and age_max == 0:
        db_df = pd.read_sql_query("SELECT * FROM book", conn_obj)
    if age_min != 0 and age_max == 0:
        query = f"""SELECT * FROM book WHERE age > {age_min}"""
        db_df = pd.read_sql_query(query, conn_obj)
    if age_min == 0 and age_max != 0:
        query = f"""SELECT * FROM book WHERE age < {age_max}"""
        db_df = pd.read_sql_query(query, conn_obj)
    if age_min != 0 and age_max != 0:
        query = f"""SELECT * FROM book WHERE age BETWEEN {age_min} AND {age_max} """
        db_df = pd.read_sql_query(query, conn_obj)
    filename = f'age_group-{str(age_min)}-{str(age_max)}-db.csv'
    db_df.to_csv(filename, index=False)
    tkinter.messagebox.showinfo("Complete",  f"{filename} saved !")


connect()
