import csv
import mysql.connector
print("1")

# Function to connect to the MySQL database
def connect_to_database():
    try:
        # Establish connection to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="Lana2008",  
            database="whale_sightings"
        )
        print("Connected to the database")
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to the database:", error)
        return None

# Function to insert sightings from a CSV file into the database
def insert_sightings_from_csv(connection, filename):
    try:
        cursor = connection.cursor()\
        with open(filename, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for row in csv_reader:
                # Extract data from the row
                sighting_date, group_size, latitude, longitude, certainty, category, mom_calf, duplicate = row
                # SQL query to insert the data into the Sightings table
                sql = "INSERT INTO Sightings (sighting_date, group_size, latitude, longitude, certainty, category, mom_calf, duplicate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (sighting_date, int(group_size), float(latitude), float(longitude), certainty, category, mom_calf, duplicate))
        # Commit the transaction
        connection.commit()
        print("Sightings inserted successfully")
    except mysql.connector.Error as error:
        print("Failed to insert sightings:", error)

def main():
    connection = connect_to_database()
    if connection:
        insert_sightings_from_csv(connection, 'C:/Users/layan/Desktop/WHALE SIGHTINGS DATASET.csv')
        connection.close()

if __name__ == "__main__":
    main()



