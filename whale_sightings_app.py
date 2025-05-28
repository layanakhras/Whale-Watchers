# Layan Akhras
# 4/28/2024
# Project Whale Watcher

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import folium


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


def plot_sightings_by_year(connection):
   query = """
   SELECT CAST(YEAR(STR_TO_DATE(sighting_date, '%d-%b-%y')) AS UNSIGNED) AS year, COUNT(*) AS num_sightings
   FROM Sightings
   GROUP BY year

   """
   result = execute_query(connection, query)
   if result:
       years = [row[0] for row in result]
       sightings = [row[1] for row in result]

       # Plotting
       plt.figure(figsize=(10, 6))
       plt.bar(years, sightings, color='lightgreen')
       plt.xlabel('Year')
       plt.ylabel('Number of Sightings')
       plt.title('Sightings by Year')
       plt.grid(axis='y', linestyle='--', alpha=0.7)
       plt.show()
   else:
       print("No results found.")


def plot_sightings_by_category(connection):
   query = """
   SELECT category, COUNT(*) AS num_sightings
   FROM Sightings
   GROUP BY category
   """
   result = execute_query(connection, query)
   if result:
       categories = [row[0] for row in result]
       sightings = [row[1] for row in result]

       plt.figure(figsize=(10, 6))
       plt.bar(categories, sightings, color='lightcoral')
       plt.xlabel('Category')
       plt.ylabel('Number of Sightings')
       plt.title('Sightings by Category')
       plt.xticks(rotation=45, ha='right')
       plt.grid(axis='y', linestyle='--', alpha=0.7)
       plt.tight_layout()
       plt.show()
   else:
       print("No results found.")


# Function to plot sightings by group size
def plot_sightings_by_group_size(connection):
   query = """
   SELECT group_size, COUNT(*) AS num_sightings
   FROM Sightings
   GROUP BY group_size
   """
   result = execute_query(connection, query)
   if result:
       group_sizes = [str(row[0]) for row in result]
       sightings = [row[1] for row in result]

       # Plotting
       plt.figure(figsize=(10, 6))
       plt.bar(group_sizes, sightings, color='orange')
       plt.xlabel('Group Size')
       plt.ylabel('Number of Sightings')
       plt.title('Sightings by Group Size')
       plt.grid(axis='y', linestyle='--', alpha=0.7)
       plt.show()
   else:
       print("No results found.")


def plot_sightings_by_mom_and_calf(connection):
   query = """
   SELECT mom_calf, COUNT(*) AS num_sightings
   FROM Sightings
   GROUP BY mom_calf
   """
   result = execute_query(connection, query)
   if result:
       categories = [row[0] for row in result]
       sightings = [row[1] for row in result]

       # Plotting
       plt.figure(figsize=(6, 6))
       plt.pie(sightings, labels=categories, autopct='%1.1f%%', startangle=140)
       plt.title('Sightings by Mom/Calf')
       plt.axis('equal')
       plt.show()
   else:
       print("No results found.")


def plot_sightings_map(connection, max_markers=5000):
   query = """
   SELECT latitude, longitude
   FROM Sightings
   """
   result = execute_query(connection, query)
   if result:
       map = folium.Map(location=[0, 0], zoom_start=2)
       markers_added = 0
       for row in result:
           lat, lon = row
           if lat is not None and lon is not None:
               folium.Marker(location=[lat, lon]).add_to(map)
               markers_added += 1
               if markers_added >= max_markers:
                   break
       if markers_added > 0:
           map.save("sightings_map.html")
           print("Map generated successfully. Check 'sightings_map.html'")
       else:
           print("No valid location data found or exceeded maximum number of markers.")
   else:
       print("No results found.")


def filter_by_certainty_and_category(connection):
   query = """
   SELECT *
   FROM Sightings AS S
   JOIN (
       SELECT sighting_id
       FROM Sightings
       WHERE CATEGORY = 'Unknown' AND CERTAINTY = 'Probable'
   ) AS U
   ON S.sighting_id = U.sighting_id
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
       print(f"Number of results: {len(result)}")
   else:
       print("No results found.")


def filter_by_certainty_and_mom_calf(connection):
   query = """
   SELECT S.*
   FROM Sightings S
   JOIN (
       SELECT DISTINCT sighting_id
       FROM Sightings
       WHERE certainty = 'Definite'
   ) AS D ON S.sighting_id = D.sighting_id
   WHERE S.mom_calf = 'Yes'
   """
   result = execute_query(connection, query)
   if result:
       for row in result:
           print(row)
       print(f"Number of results: {len(result)}")
   else:
       print("No results found.")



def main():
   df = pd.read_csv("C:/WHALE SIGHTINGS/WHALE SIGHTINGS DATASET.csv")
   connection = connect_to_database()
   if connection:
       insert_sightings_data(connection, df)

       while True:
           print("\n=== Whale Watcher ===")
           print("1. Find sightings by certainty")
           print("2. Find sightings by observer")
           print("3. Find sightings by group size")
           print("4. Find sightings by year")
           print("5. Find sightings with Mom-and-Calf pair")
           print("6. Filter by highest group size")
           print("7. Find sightings with unknown observer and probable certainty")
           print("8. Find sightings with mom and calf pair and definite certainty")
           print("9. Find sightings by exact date")
           print("10. Generate sighting chart by month")
           print("11. Generate sighting chart by year")
           print("12. Generate sighting chart by observer")
           print("13. Generate sighting chart by group size")
           print("14. Generate mom/calf sighting chart")
           print("15. Generate sightings map")
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
               print("Fetching sightings with unknown observer and probable certainty...")
               filter_by_certainty_and_category(connection)
           elif choice == "8":
               print("Fetching definite sightings of mom and calf pair...")
               filter_by_certainty_and_mom_calf(connection)
           elif choice == "9":
               day = int(input("Enter day (1-31): "))
               month = int(input("Enter month (1-12): "))
               year = int(input("Enter year (2002-2018): "))
               filter_by_date(connection, day, month, year)
           elif choice == "10":
               plot_sightings_by_month(connection)
           elif choice == "11":
               plot_sightings_by_year(connection)
           elif choice == "12":
               plot_sightings_by_category(connection)
           elif choice == "13":
               plot_sightings_by_group_size(connection)
           elif choice == "14":
               plot_sightings_by_mom_and_calf(connection)
           elif choice == "15":
               plot_sightings_map(connection)
           elif choice == "0":
               break
           else:
               print("Invalid choice. Please try again.")

       connection.close()
   print("Goodbye!")


if __name__ == "__main__":
   main()

