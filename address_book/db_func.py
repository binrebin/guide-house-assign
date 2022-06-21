import sqlite3
import csv


def connect():
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    cur_obj.execute("CREATE TABLE IF NOT EXISTS "
                    "book (id integer PRIMARY KEY, "
                    "fname text, "
                    "mname text, "
                    "lname text, "
                    "addr_1 text, "
                    "city text,"
                    "state text,"
                    "ph_num text)")
    conn_obj.commit()
    conn_obj.close()


def insert(fname, mname, lname, addr_1, city, state, ph_num):
    conn_obj = sqlite3.connect("addressbook.db")
    cur_obj = conn_obj.cursor()
    cur_obj.execute("INSERT INTO book "
                    "VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)", (fname, mname, lname, addr_1, city, state, ph_num))
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


def download_csv():
    pass


connect()
