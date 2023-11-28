import mysql.connector
import numpy as np
import pymongo
import time

while True:

    time.sleep(15)

    try:
        db = mysql.connector.connect(
            host="mysql-db",
            user="root",
            password="P@ssw0rd",
            database="users"
        )

        cursor = db.cursor()

        sql = "SELECT grade FROM data"

        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()
        db.close()

        if result != []:

        # print(result)

            grade_list = []

            for value in result:
                grade_list.append(value[0])

            grade_max = max(grade_list)
            grade_min = min(grade_list)
            grade_mean = np.mean(grade_list)
            grade_median = np.median(grade_list)
            grade_count = len(grade_list)

            print(f"{grade_max} {grade_min} {grade_mean} {grade_median}")

            mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")

            dblist = mongo_client.list_database_names()
            if "db1" not in dblist:
                print("The database exists.")

            mongo_db = mongo_client["db1"]
            mongo_col = mongo_db["students"]

            data = {
                "name": "stats",
                "grade_max": grade_max,
                "grade_min": grade_min,
                "grade_mean": grade_mean,
                "grade_median": grade_median,
                "grade_count": grade_count
            }
            if mongo_col.find_one() == None:
                x = mongo_col.insert_one(data)
            else:
                query = {"name": "stats"}
                new_val = {"$set": data}
                mongo_col.update_one(query, new_val)

            mongo_client.close()
    except:
        print("there was an error")

    time.sleep(15)
