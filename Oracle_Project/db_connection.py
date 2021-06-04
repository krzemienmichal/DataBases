import cx_Oracle
import config


def add_clients(data, cursor, cnx):
    try:
        #query = """insert into client values(NULL,"""
        cursor.callproc("ADDCLIENT", list(data))
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def delete_clients(c_id, cursor, cnx):
    try:
        cursor.callproc("DELETE_CLIENT", (c_id,))
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def update_clients(cursor, cnx, data=("", "", "", "", "", "", "")):
    try:
        cursor.callproc("UPDATECLIENT", data[0:6])
        if data[6] != "":
            cursor.callproc("CHANGE_PASSWORD", data[6])
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def add_movies(cursor, cnx, title, data, genre_data):
    try:
        try:
            cursor.callproc("ADD_MOVIE", data)
        except cx_Oracle.Error as err:
            cnx.rollback()
            return err
        try:
            for item in list(genre_data):
                print(item)
                gen_dat = (title, item)
                print(gen_dat)
                cursor.callproc("ADD_MOVIE_GENRE", gen_dat)
            return None
        except cx_Oracle.Error as err:
            cnx.rollback()
            return err
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def add_genre_to_movies(cursor, cnx, title, genre_data):
    try:
        for item in list(genre_data):
            gen_dat = (title, item)
            cursor.callproc("ADD_MOVIE_GENRE", gen_dat)
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def delete_genre_from_movies(cursor, cnx, title, genre_data):
    try:
        for item in list(genre_data):
            gen_dat = (title, item)
            cursor.callproc("RM_GEN_MOVIE", gen_dat)
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def delete_movies(title, cursor, cnx):
    try:
        query = """DELETE FROM movie WHERE movie.Title = %s"""
        cursor.execute(query, (title,))
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def update_movies(cursor, cnx, data=("", "", "", "", "")):
    try:
        cursor.callproc("Update_Movie", data)
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def list_clients(cursor, cnx):
    try:
        query = "SELECT * FROM list_clients"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err, None


def list_movies(cursor, cnx):
    try:
        query = "SELECT * FROM list_movies"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def list_genres(cursor, cnx):
    try:
        query = "SELECT * FROM list_genres"
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def show_watched_for_all_users(cursor, cnx):
    try:
        query = """SELECT * FROM list_watched"""
        cursor.execute(query)
        data = cursor.fetchall()
        return None, data
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def show_ptw_for_all_users(cursor, cnx):
    try:
        query = """SELECT * FROM list_ptw"""
        cursor.execute(query)
        data = cursor.fetchall()
        cnx.commit()
        return None, data
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def add_ptw(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("ADD_PTW", gen_dat)
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def remove_ptw(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("RM_PTW", gen_dat)
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def add_watched(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("ADD_WATCHED", gen_dat)
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err


def remove_watched(cursor, cnx, data):
    try:
        for item in list(data[1:]):
            gen_dat = (data[0], item)
            cursor.callproc("RM_WATCHED", gen_dat)
        return None
    except cx_Oracle.Error as err:
        cnx.rollback()
        return err

def db_connect():
    cnx = None
    try:
        cnx = cx_Oracle.connect(
            config.username,
            config.password,
            config.dsn,
            encoding=config.encoding)

        print(cnx.version)
    except cx_Oracle.Error as err:
        return err
    finally:
        if cnx:
            cursor = cnx.cursor()
            return None, cnx, cursor


def main():
    err, cnx, cursor = db_connect()
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    main()
