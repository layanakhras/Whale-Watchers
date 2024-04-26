import mysql.connector
import pandas as pd


def connect_to_database():
   try:
       connection = mysql.connector.connect(
           host="localhost",
           user="root",
           password="Lana2008",
           database="whale_sightings"
       )
       print("Connected to MySQL successfully!")
       return connection
   except mysql.connector.Error as err:
       print("Error connecting to MySQL:", err)
       return None


def execute_query(connection, query):
   cursor = connection.cursor()
   try:
       cursor.execute(query)
       result = cursor.fetchall()
       cursor.close()
       return result
   except mysql.connector.Error as err:
       print("Error executing query:", err)
       return None


def example_query(connection):
   query = """
   SELECT Sightings.sighting_id, Sightings.sighting_date, Category.category_name
   FROM Sightings
   JOIN Category ON Sightings.category = Category.category_name
   LIMIT 10
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
   else:
       print("No results found")


def insert_sightings_data(connection, df):
   cursor = connection.cursor()
   for index, row in df.iterrows():
       query = """
       INSERT INTO Sightings (sighting_date, group_size, latitude, longitude, certainty, category, mom_calf, duplicate)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
       """
       values = (
           row['SIGHTINGDATE'],
           row['GROUPSIZE'],
           row['LAT'],
           row['LON'],
           row['CERTAINTY'],
           row['CATEGORY'],
           row['MOM_CALF'],
           row['DUPLICATE']
       )
       cursor.execute(query, values)
       connection.commit()
   cursor.close()


def main():
   df = pd.read_csv("C:/WHALE SIGHTINGS/WHALE SIGHTINGS DATASET.csv")
   connection = connect_to_database()
   if connection:
       insert_sightings_data(connection, df)
       example_query(connection)
       connection.close()
       print("Data insertion and example query completed.")
   print("End Program")


if __name__ == "__main__":
   main()


