import sqlite3 as sq
from sqlite3 import Error

ab_database = r'C:\Users\petrv\Documents\Pyladies\Laber_maker_02\db\ab_database.db'

# TODO: zajistit, aby se po stažení udělala cesta/adresář s databází

def bac_database_con():
    data = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("Connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS bacteria (
                                    name text);""")  # vytvoření tabulky
        conn.commit()
        cur.execute("SELECT * FROM bacteria")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
            print(row)
    except Error as e:
        print(e)
    data.sort()
    print("Bacteria table: ", data)
    return data


def add_bac(item):
    entries = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS bacteria(
                                    name text);""")  # vytvoření tabulky
        conn.commit()
        entries.clear()
        entries.append(item)
        print(entries)
        cur.executemany("INSERT INTO bacteria VALUES(?)", zip(entries))
        conn.commit()
        conn.close()
        # print("done")
    except Error as e:
        print(e)
    print("New bacteria added to table", entries)


def delete_bac(no):
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        sql = "DELETE FROM bacteria WHERE name = '" + str(no) + "'"
        cur.execute(sql)
        conn.commit()
        print(f"Bacteria {no} deleted from table")
    except Error as e:
        print(e)


def cell_culture_database_con():
    data = []
    try:
        conn = sq.connect(ab_database)
        print("connected to database", sq.version)
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS cell_line (
                                name text PRIMARY KEY,
                                medium text);""")
        conn.commit()
        cur.execute("SELECT * FROM cell_line")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
            print(row)
    except Error as e:
        print(e)
    data.sort()
    print("Cell lines table: ", data)
    return data


def add_cell_culture(item):
    entries = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS cell_line(
                                    name text PRIMARY KEY,
                                    media text);""")  # vytvoření tabulky
        conn.commit()
        entries.clear()
        entries.append(item)
        print(entries)
        cur.executemany("INSERT INTO cell_line VALUES(?, ?)", entries)
        conn.commit()
        # print("hotovo")
    except Error as e:
        print(e)
    print("New cell line added to table", entries)
    return entries


def delete_cell_culture(name):
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        sql = "DELETE FROM cell_line WHERE name = '" + str(name) + "'"
        cur.execute(sql)
        conn.commit()
        print(f"Cell line {name} deleted from table")
    except Error as e:
        print(e)


def project_database_con():
    data = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected database", sq.version)
        cur = conn.cursor()  # umožní zapisování/čtení do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS projects(
                            no int PRIMARY KEY,
                            name text,
                            finished text);""")  # vytvoření tabulky, pokud už není
        conn.commit()
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
    except Error as e:
        print(e)
    data.sort()
    print("Projects table: ", data)
    return data


def add_project(item):
    entries = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS projects(
                                no int PRIMARY KEY,
                                name text,
                                finished text);""")  # vytvoření tabulky
        conn.commit()
        entries.clear()
        entries.append(item)
        print(entries)
        cur.executemany("INSERT INTO projects VALUES(?, ?, ?)", entries)
        conn.commit()
        # print("hotovo")
    except Error as e:
        print(e)
    print("New project added to table", entries)
    return entries


def delete_project(no):
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        sql = "DELETE FROM projects WHERE no = " + str(no)
        cur.execute(sql)
        conn.commit()
        print(f"Project {no} deleted from table", no)
    except Error as e:
        print(e)


def protein_database_con():
    data = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("Connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS proteins (
                                    unit text);""")  # vytvoření tabulky
        conn.commit()
        cur.execute("SELECT * FROM proteins")
        rows = cur.fetchall()
        for row in rows:
            data.append(row)
            print(row)
    except Error as e:
        print(e)
    data.sort()
    print("Proteins table: ", data)
    return data

def add_unit(item):
    entries = []
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        cur.execute("""CREATE TABLE IF NOT EXISTS proteins(
                                        unit text);""")  # vytvoření tabulky
        conn.commit()
        entries.clear()
        entries.append(item)
        print(entries)
        cur.executemany("INSERT INTO proteins VALUES(?)", zip(entries))
        conn.commit()
        conn.close()
        # print("done")
    except Error as e:
        print(e)
    print("New bacteria added to table", entries)

def delete_unit(no):
    try:
        conn = sq.connect(ab_database)  # vytvoří spojení s databází
        print("connected to database", sq.version)
        cur = conn.cursor()  # umožní zapisování do dazabáze
        sql = "DELETE FROM proteins WHERE unit = '" + str(no) + "'"
        cur.execute(sql)
        conn.commit()
        print(f"Unit {no} deleted from table")
    except Error as e:
        print(e)

