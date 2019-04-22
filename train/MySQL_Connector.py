import mysql.connector

password=''
def connect_to_database():
    msd = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='msd'
    )

    mxm = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='mxm'
    )

    mbzdb = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='mbzdb'
    )

    return msd, mxm, mbzdb


def get_output_from_database(database, query):
    cur = database.cursor()
    cur.execute(query)
    output = cur.fetchall()
    return output




