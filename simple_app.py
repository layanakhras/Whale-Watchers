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
   except mysql.connection.Error as err:
      print("Error connecting to MySQL:", err)
      return None

def main():
   connection = connect_to_database()
   if connection:
      
      connection.close()

if __name__ == "__main__":
   main()
