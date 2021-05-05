import mysql.connector


def show_city_info():
    query = "SELECT ID, Name, CountryCode, District, Population FROM city"
    cursor.execute(query)
    for (ID, Name, CountryCode, District, Population) in cursor:
        print(ID, Name, CountryCode, District, Population)


def insert_city():
    query = ("INSERT INTO city(Name, CountryCode)"
             "VALUES(%s, %s)")

    name = input('City name: ')
    country_code = input('CountryCode: ')
    city_data = (name, country_code)
    print(city_data)
    cursor.execute(query, city_data)
    cnx.commit()


def update_population():
    query = ('''UPDATE city
                SET Population = Population + %s
                WHERE Name = %s''')
    city_population = input("Update population by inserted number: ")
    city_name = input("City name: ")
    cursor.execute(query, (city_population, city_name))
    cnx.commit()


def delete_city():
    query = ('''DELETE FROM city
    WHERE Name = %s;
    ''')
    city_name = input("Insert city name to delete: ")
    cursor.execute(query, (city_name,))
    cnx.commit()


if __name__ == "__main__":
    cnx = mysql.connector.connect(user='username', password='password',
                                  host='host',
                                  database='world')
    cursor = cnx.cursor()
    while True:
        print("""Choose what you want to do:
           1. Add city to the table
           2. Show all cities
           3. Update population of chosen city
           4. Delete chosen city
           5. Exit
           """)
        option = input()
        if option == '1':
            insert_city()
        elif option == '2':
            show_city_info()
        elif option == '3':
            update_population()
        elif option == '4':
            delete_city()
        elif option == '5':
            cursor.close()
            cnx.close()
            exit()
        else:
            print("You chose wrong option")
