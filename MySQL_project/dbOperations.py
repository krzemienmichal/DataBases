import mysql.connector


def add_clients(data, cursor, cnx):
    try:
        cnx.start_transaction()
        cursor.callproc("AddClient", data)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def delete_clients(c_id, cursor, cnx):
    try:
        cnx.start_transaction()
        cursor.callproc("DeleteClient", (c_id,))
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def update_clients(cursor, cnx, data=("", "", "", "", "", "", "")):
    try:
        cnx.start_transaction()
        cursor.callproc("UpdateClient", data[0:6])
        if data[6] != "":
            cursor.callproc("ChangePassword", data[6])
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def add_movies(cursor, cnx, title, data, genre_data):
    try:
        try:
            cursor.callproc("AddMovie", data)
        except mysql.connector.Error as err:
            cnx.rollback()
            return err
        try:
            for item in list(genre_data):
                print(item)
                gen_dat = (title, item)
                print(gen_dat)
                cursor.callproc("AddGenreToMovie", gen_dat)
            return None
        except mysql.connector.Error as err:
            cnx.rollback()
            return err
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def add_genre_to_movies(cursor, cnx, title, genre_data):
    try:
        for item in list(genre_data):
            gen_dat = (title, item)
            cursor.callproc("AddGenreToMovie", gen_dat)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def delete_genre_from_movies(cursor, cnx, title, genre_data):
    try:
        for item in list(genre_data):
            gen_dat = (title, item)
            cursor.callproc("RemoveGenreFromMovie", gen_dat)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def delete_movies(title, cursor, cnx):
    try:
        cnx.start_transaction()
        query = """DELETE FROM `movie` WHERE `movie`.Title = %s"""
        cursor.execute(query, (title,))
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def update_movies(cursor, cnx, data=("","","","","")):
    try:
        cnx.start_transaction()
        cursor.callproc("UpdateMovie", data)
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def list_clients(cursor, cnx):
    try:
        cnx.start_transaction()
        query = "SELECT * FROM listclients;"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except mysql.connector.Error as err:
        cnx.rollback()
        return err, None


def list_movies(cursor, cnx):
    try:
        query = "SELECT * FROM list_movies"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def list_genres(cursor, cnx):
    try:
        query = "SELECT * FROM list_genres"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def show_watched_for_all_users(cursor, cnx):
    try:
        query = """SELECT * FROM list_watched"""
        cursor.execute(query)
        data = cursor.fetchall()
        return None, data
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def show_ptw_for_all_users(cursor, cnx):
    try:
        query = """SELECT * FROM list_ptw"""
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def add_ptw(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("AddPtw", gen_dat)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def remove_ptw(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("RemovePtw", gen_dat)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def add_watched(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("AddWatched", gen_dat)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def remove_watched(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("RemoveWatched", gen_dat)
        return None
    except mysql.connector.Error as err:
        cnx.rollback()
        return err


def db_connect(user='', password='', host='', database='mkproject'):
    try:
        cnx = mysql.connector.connect(user=user, password=password,
                                      host=host,
                                      database=database)
        cursor = cnx.cursor()
        return None, cnx, cursor
    except mysql.connector.Error as err:
        return err


def main():
    err, cnx, cursor = db_connect()
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
