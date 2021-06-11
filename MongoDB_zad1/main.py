from connection import Connect
from pymongo import MongoClient
import datetime
import pprint
import os

client = Connect.get_connection()
db = client.bd_studies

collection = db.workers
db.list_collection_names()

# for i in collection.find():
#     pprint.pprint(i)


mydict = { "name": "Peter", "address": "Lowstreet 27" }
if __name__ == "__main__":
    while True:

        print("""
1. Add data
2. Read all data
3. Update data
4. Delete data
5. Exit

""")

        option = input("Insert option: ")

        if option == "1":
            worker = {
                "id": int(input("Insert worker id: ")),
                "name": input("Name: "),
                "surname": input("surname:"),
                "birth date": datetime.datetime(int(input("Year: ")),
                                                int(input("Month: ")),
                                                int(input("Day: ")),
                                                0, 0),
                "PESEL": (input("PESEL: ")),
                "address": {"post code" : input("postal code: "),
                            "city": input("city: "),
                            "street": input("street: ")},
                "phone number": int(input("phone number: ")),
                "mail address": input("email: "),
                "department": input("department: "),
                "manager_id": int(input("manager_id: ")),
                "forma zatrudnienia": input("forma zatrudnienia: ")
            }
            collection.insert_one(worker)
        elif option == "2":
            for result in collection.find():
                pprint.pprint(result)
        elif option == "3":
            collection.update_one({"id":int(input("ID to update: "))},
                                  {"$set":{input("What field to update") : input("value: ")}})
        elif option == "4":
            collection.delete_one({"id": int(input("ID to delete"))})
        elif option == "5":
            break