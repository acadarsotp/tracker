import urllib3
from urllib3 import exceptions
import mysql.connector
from tqdm import tqdm


# Function to ask the user if the celestrak database should be updated
def askupdate():
    choice = input("\nDo you want to download new satellite data? (y/n): ")
    if choice.lower() == "y":
        update_data()
    elif choice.lower() == "n":
        return
    else:
        print("\nPlease answer with y or n.")
        return askupdate()


# Function to parse the TLE file and extract the satellite data, returns true if the access is denied or false if
# access is granted.
def get_data():
    try:
        satellites = []
        http = urllib3.PoolManager()
        response = http.request('GET', "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")
        data = response.data.decode('utf-8')
        lines = data.splitlines()
    except urllib3.exceptions.MaxRetryError:
        print("Unable to reach celestrak.com, try again")
        return True, askupdate()

    if len(lines) < 1000:
        print("\nAccess blocked by celestrak due to too many downloads, try again later.")
        return True, askupdate()
    print("\nDownloading celestrak data")
    idcounter = 0
    for i in range(0, len(lines), 3):
        # Extract satellite name and TLE data
        name = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()

        # Create a dictionary to store satellite data
        sat = {'id': idcounter, 'name': name, 'line1': line1, 'line2': line2}
        satellites.append(sat)
        idcounter = idcounter + 1
    return False, satellites


# Function to get the data to SQL database
def update_data():
    """
    # Connect to the MySQL server and create a database
    mydb = mysql.connector.connect(
        host="localhost",
        user="YOUR USER",
        password="YOUR PASSWORD"
    )
    mycursor = mydb.cursor()
    #mycursor.execute("DROP DATABASE celestrak")
    mycursor.execute("CREATE DATABASE celestrak")
    """

    """
    # Create a table to store the satellite data
    mycursor.execute(
        "CREATE TABLE satellites (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), line1 VARCHAR(255),"
        "line2 VARCHAR("
        "255))")
    """

    # Parse the TLE file and insert the satellite data into the table
    access_blocked, satellites = get_data()
    if not access_blocked:
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="YOUR USER",
            password="YOUR PASSWORD",
            database="celestrak"
        )
        mycursor = mydb.cursor()

        # Delete the old data
        mycursor.execute("DELETE FROM satellites")

        # Update new data
        print("Updating data to MySQL Database")
        sql = "REPLACE INTO satellites (id, name, line1, line2) VALUES (%s, %s, %s, %s)"
        val = [(sat['id'], sat['name'], sat['line1'], sat['line2']) for sat in tqdm(satellites)]
        mycursor.executemany(sql, val)
        # Commit the changes and close the database connection
        mydb.commit()
        mydb.close()
        return
    else:
        # The database is not modified if access to the data was blocked
        return
