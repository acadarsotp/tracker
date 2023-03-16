import mysql.connector
import ephem
from math import *


def search():
    # Confirm observer coordinates
    defaultgroundcoord = ("43.37135", "-8.396", 0)
    print("\nDefault observer coordinates -> LAT =", defaultgroundcoord[0], "| LON =", defaultgroundcoord[1],
          "| HEIGHT =", defaultgroundcoord[2])
    confirm = input("\nDo you want to set new ground coordinates? (y/n): ")
    if confirm.lower() == "y":
        lat = input("\nEnter latitude: ")
        lon = input("Enter longitude: ")
        elev = input("Enter elevation (in meters): ")
        try:
            lat = float(lat)
            lon = float(lon)
            elev = float(elev)
            if (-90 <= lat <= 90) and (-180 <= lon <= 180):
                groundcoord = (str(lat), str(lon), float(elev))
                print("\nNew observer coordinates -> LAT =", groundcoord[0], "| LON =",
                      groundcoord[1], "| HEIGHT =", groundcoord[2])
            else:
                print("\nInvalid Coordinates")
                return search()
        except ValueError:
            print("\nInvalid Coordinates")
            return search()
    elif confirm.lower() == "n":
        groundcoord = defaultgroundcoord  # default coordinates
    else:
        print("\nPlease choose y or n")
        return search()

    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="celestrak"
    )

    # Create a cursor object to execute queries
    cursor = db.cursor()

    # Get user input for satellite name
    sat_name = input("\nEnter satellite name: ")

    # Select all satellite names that are similar to the user input
    cursor.execute("SELECT name FROM satellites WHERE name LIKE %s", ("%" + sat_name + "%",))
    results = cursor.fetchall()

    # If no results found, notify the user and exit
    if len(results) == 0:
        print("\nNo matching satellites found, try again.")
        db.close()
        return search()

    # Display list of similar satellite names and ask user to choose one
    print("\nChoose a satellite:")
    for i, row in enumerate(results):
        print(f"{i + 1}. {row[0]}")
    print(f"{len(results) + 1}.", "BACK TO SEARCH")
    try:
        choice = int(input("\nEnter number of choice: "))

        if choice <= 0:
            print("Your input does not correspond to any of the satellites of the provided list, try again.")
            db.close()
            return search()

        if choice == len(results) + 1:
            db.close()
            return search()

        # Get the TLE of the chosen satellite

        chosen_sat_name = results[choice - 1][0]
        cursor.execute("SELECT line1, line2 FROM satellites WHERE name = %s", (chosen_sat_name,))
        result = cursor.fetchone()
        line1 = result[0]
        line2 = result[1]
    except IndexError:
        print("Your input does not correspond to any of the satellites of the provided list, try again.")
        db.close()
        return search()
    except ValueError:
        print("Your input does not correspond to any of the satellites of the provided list, try again.")
        db.close()
        return search()

    # Ask user to confirm that they want to track the chosen satellite
    try:
        # print(f"\nNext pass for {chosen_sat_name}:")
        sat = ephem.readtle(chosen_sat_name, line1, line2)
        observer = ephem.Observer()
        observer.lat = groundcoord[0]
        observer.lon = groundcoord[1]
        observer.elevation = groundcoord[2]
        next_pass = observer.next_pass(sat)
        sat.compute(observer)
    except ValueError:
        print("Unable to compute pass over objective, this satellite may never go over your horizon.")
        db.close()
        return search()

    if degrees(sat.alt) > 0:
        print("\nPass ongoing with an elevation of:", degrees(sat.alt))

    print(f"\nNext pass for {chosen_sat_name}:")
    print(f"Rise time UTC: {next_pass[0]}")
    print(f"Set time UTC: {next_pass[4]}")
    confirm = input(f"\nTrack {chosen_sat_name}? (y/n): ")

    # If user confirms, extract TLE into a dictionary

    if confirm.lower() == "y":
        tle_dict = {"name": chosen_sat_name, "tle1": line1, "tle2": line2}
        db.close()
        return groundcoord, tle_dict
    elif confirm.lower() == "n":
        db.close()
        return search()
    else:
        print("Please choose y or n")
        db.close()
        return search()
