import mysql.connector
import pandas as pd


# Function to connect to the MySQL database
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


# Function to execute SQL queries
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


# Function to insert data into the database
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


# Function to filter by certainty
def filter_by_certainty(connection, certainty):
   query = f"""
   SELECT *
   FROM Sightings
   WHERE certainty = '{certainty}'
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
   else:
       print("No results found.")


# Function to filter by category
def filter_by_category(connection, category):
   query = f"""
   SELECT *
   FROM Sightings
   WHERE category = '{category}'
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
   else:
       print("No results found.")


# Function to filter by group size
def filter_by_group_size(connection, group_size):
   query = f"""
   SELECT *
   FROM Sightings
   WHERE group_size = {group_size}
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
   else:
       print("No results found.")


# Main function
def main():
   df = pd.read_csv("C:/WHALE SIGHTINGS/WHALE SIGHTINGS DATASET.csv")
   connection = connect_to_database()
   if connection:
       insert_sightings_data(connection, df)

       # Text-based user interface
       while True:
           print("\n=== Whale Sightings Menu ===")
           print("1. Filter by Certainty")
           print("2. Filter by Category")
           print("3. Filter by Group Size")
           print("4. Exit")
           choice = input("Enter your choice: ")

           if choice == "1":
               certainty = input("Enter certainty: ")
               filter_by_certainty(connection, certainty)
           elif choice == "2":
               category = input("Enter category: ")
               filter_by_category(connection, category)
           elif choice == "3":
               group_size = int(input("Enter group size: "))
               filter_by_group_size(connection, group_size)
           elif choice == "4":
               print("Exiting the program.")
               break
           else:
               print("Invalid choice. Please try again.")

       connection.close()
       print("Data manipulation completed.")
   print("End Program")


if __name__ == "__main__":
   main()

