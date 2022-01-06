import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_row(conn, travel_data):
    sql = "INSERT INTO travel_data(milesAway, l2, percentage, speed, tempWarm, tempCold ) VALUES(?,?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, (travel_data.milesAway,
                      travel_data.l2,
                      travel_data.percentage,
                      travel_data.speed,
                      travel_data.tempWarm,
                      travel_data.tempCold,))
    return cur.lastrowid


def main(conn):
    sql_create_travel_data_table = '''CREATE TABLE IF NOT EXISTS travel_data (
                                    id integer PRIMARY KEY, 
                                    milesAway float NOT NULL, 
                                    l2 float NOT NULL, 
                                    percentage float NOT NULL, 
                                    speed float NOT NULL, 
                                    tempWarm float NOT NULL, 
                                    tempCold float NOT NULL)'''
    with conn:
        create_table(conn, sql_create_travel_data_table)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def update(conn, travel_data):
    with conn:
        create_row(conn, travel_data)


def select_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM travel_data")
    rows = cur.fetchall()
    return rows
