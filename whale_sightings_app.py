import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


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
   print("Loading data...")
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
   print("Loading complete")


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
       print(f"Number of results: {len(result)}")
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
       print(f"Number of results: {len(result)}")
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
       print(f"Number of results: {len(result)}")
   else:
       print("No results found.")


def filter_by_year(connection, year):
   query = f"""
   SELECT *
   FROM Sightings
   WHERE YEAR(STR_TO_DATE(sighting_date, '%d-%b-%y')) = {year}
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
       print(f"Number of results: {len(result)}")
   else:
       print("No results found.")


def filter_by_mom_and_calf(connection):
   query = """
   SELECT *
   FROM Sightings
   WHERE mom_calf = 'Yes'
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
       print(f"Number of results: {len(result)}")
   else:
       print("No mom and calf sightings found.")


def highest_group_size(connection):
   query = """
   SELECT S.*
   FROM Sightings AS S
   JOIN (
       SELECT MAX(group_size) AS max_group_size
       FROM Sightings
   ) AS max_size
   ON S.group_size = max_size.max_group_size
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
       print(f"Number of results: {len(result)}")
   else:
       print("No results found.")


def filter_by_date(connection, day, month, year):
   query = f"""
   SELECT *
   FROM Sightings
   WHERE DAY(STR_TO_DATE(sighting_date, '%d-%b-%y')) = {day}
   AND MONTH(STR_TO_DATE(sighting_date, '%d-%b-%y')) = {month}
   AND YEAR(STR_TO_DATE(sighting_date, '%d-%b-%y')) = {year}
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
       print(f"Number of results: {len(result)}")
   else:
       print("No results found for the specified date.")


def plot_sightings_by_month(connection):
   query = """
   SELECT MONTH(STR_TO_DATE(sighting_date, '%d-%b-%y')) AS month, COUNT(*) AS num_sightings
   FROM Sightings
   GROUP BY month
   """
   result = execute_query(connection, query)
   if result:
       months = [row[0] for row in result]
       sightings = [row[1] for row in result]

       # Plotting
       plt.figure(figsize=(10, 6))
       plt.bar(months, sightings, color='skyblue')
       plt.xlabel('Month')
       plt.ylabel('Number of Sightings')
       plt.title('Sightings by Month')
       plt.xticks(range(1, 13))
       plt.grid(axis='y', linestyle='--', alpha=0.7)
       plt.show()
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
           print("\n=== Whale Watcher ===")
           print("1. Filter by Certainty")
           print("2. Filter by Category")
           print("3. Filter by Group Size")
           print("4. Filter by Year")
           print("5. Filter by Mom and Calf")
           print("6. Filter by highest group size")
           print("7. Filter by date")
           print("8. View sighting chart by month ")
           print("0. Exit")
           print("========================")
           choice = input("Enter your choice: ")

           if choice == "1":
               print("Certainties: [Definite, Probable]")
               certainty = input("Enter certainty: ")
               filter_by_certainty(connection, certainty)
           elif choice == "2":
               print("Categories: ")
               print("[US Coast Guard, Dedicated Eg Aerial, Opportunistic, Commercial vessel, Fishing Vessel,")
               print("Volunteer Sighting Network, Dedicated Eg Shipboard, Unknown, Whale watch, Acoustic]")
               category = input("Enter category:")
               filter_by_category(connection, category)
           elif choice == "3":
               print("Group sizes: [1-100]")
               group_size = int(input("Enter group size: "))
               filter_by_group_size(connection, group_size)
           elif choice == "4":
               print("Years: [2002-2018]")
               year = int(input("Enter year: "))
               filter_by_year(connection, year)
           elif choice == "5":
               print("Mom and Calf Sightings: ")
               filter_by_mom_and_calf(connection)
           elif choice == "6":
               print("Fetching sightings with the highest recorded group size...")
               highest_group_size(connection)
           elif choice == "7":
               day = int(input("Enter day (1-31): "))
               month = int(input("Enter month (1-12): "))
               year = int(input("Enter year (2002-2018): "))
               filter_by_date(connection, day, month, year)
           elif choice == "8":
               plot_sightings_by_month(connection)
           elif choice == "0":
               print("Exiting the program.")
               break
           else:
               print("Invalid choice. Please try again.")

       connection.close()
   print("End Program")


if __name__ == "__main__":
   main()

