# destination_manager.py

import sqlite3
from tabulate import tabulate

class DestinationManager:
    def __init__(self, connection):
        self.conn = connection
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

# 1. View a list of all existing destinations, sorted by city. 
    def view_destination(self):
        self.cursor.execute("""
        SELECT name, city, country, iata_code
        FROM airport
        ORDER BY country""")
        destination_rows = self.cursor.fetchall()

#build table to return to user
        if destination_rows:
            destination_headers = ['Airport', 'City', 'Country', 'IATA Code']
            print('\n--- Destinations ---')
            print(tabulate(destination_rows, headers=destination_headers, tablefmt='grid'))
        else:
            print('No destinations found.')
        
        input('\nPress Enter to return to the Destination Menu.') 

# 2. Adding destination: add a new destination to the database
    def add_destination(self):
        print('\n--- Add a New Destination ---')

        while True: 
            name = input('Enter Airport Name: ').strip()
            city = input('Enter City: ').strip()
            country = input('Enter Country (please provide the full name with no abbreviations): ').strip()
            iata_code = input('Enter IATA code (3 letters): ').strip().upper()

#Adding destination: this makes all fields mandatory and ensures that the IATA code is 3 letters.
            if name and city and country and len(iata_code) == 3:
                break #valid input, exit the loop
            else:
                print('\nInvalid input. All fields are required, and IATA code must be 3 letters.')
                input('Press Enter to return to the Destination Menu.') 
                return
        
        try:
            self.cursor.execute("""
                INSERT INTO airport (name, city, country, iata_code)
                VALUES (?, ?, ?, ?)
            """, (name, city, country, iata_code))
            self.conn.commit()
            print(f"\nDestination '{name}' added successfully")

#The user may try to add a new destination, however it may already exist. 
#If this happens, the user will be told. If other error messages are thrown, the user can return to the Destination menu. 

        except sqlite3.IntegrityError as retry:
            if 'UNIQUE constraint failed: airport.iata_code' in str(retry):
                print('\nA destination with that IATA code already exists.\n')
                input('Press Enter to return to the Destination Menu.')
                return
            else:
                print(f"Database error: {retry}")
                input('\nPress Enter to return to the Destination Menu.')
                return
            
#3. Updating existing Destination by inputting IATA code
    def update_destination(self):
        print('\n--- Update a Destination ---')
        iata_code = input('IATA code: ').strip().upper()

#Updating destination - only 3 letters will be accepted
        if len(iata_code) != 3:
            print('\nInvalid IATA code. It must be 3 letters.')
            input('Press Enter to return to the Destination Menu.') 
            return

#check if the IATA code is already in the database
        self.cursor.execute("""
            SELECT name, city, country 
            FROM airport WHERE iata_code = ?
        """, (iata_code,))
        code_row = self.cursor.fetchone()

        if not code_row:
            print(f"No destination found with IATA code '{iata_code}'.")
            return
        
        print(f'\nCurrent Information: Airport: {code_row[0]}, City: {code_row[1]}, Country: {code_row[2]}')

#request new values, if the IATA code is not found in the flight database. If the user doesn't enter a value, then keep the current one. 
        new_name = input('Enter new airport name (leave blank to keep current): ').strip()
        new_city = input('Enter new city (leave blank to keep current): ').strip()
        new_country = input('Enter new country (leave blank to keep current): ').strip()

#if the user doesn't enter a new value, keep the current one 
        new_name = new_name or code_row[0]
        new_city = new_city or code_row[1]
        new_country = new_country or code_row[2]

        try:
            self.cursor.execute("""
            UPDATE airport
            SET name = ?, city = ?, country = ?
            WHERE iata_code = ?
            """, (new_name, new_city, new_country, iata_code))
            self.conn.commit()
            print(f"\nDestination '{iata_code}' updated successfully.")
        except sqlite3.IntegrityError as e:
            print(f'Error: {e}')
        
        input('Press Enter to return to the Destination Menu.') 

#4. delete destination, but only if it is not in use in any flights. 
    
    def delete_destination(self):
        print("\n=== Delete Destination ===")
        iata_code = input("Enter the IATA code of the destination to delete: ").strip().upper()

        # Check if the destination exists
        self.cursor.execute("""
            SELECT * FROM airport 
                WHERE iata_code = ?
        """, (iata_code,))
        destination = self.cursor.fetchone()

        if not destination:
            print("Destination not found.")
            return
        
#destinations cannot be deleted if they are used in existing flights. 

#checks the origin and destinations of existing flights.        
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM flight
            WHERE origin_id = ? OR destination_id = ?
        """, (iata_code, iata_code))

        flight_count = self.cursor.fetchone()[0]

#error message is returned if the destination is used in an existing flight. 
        if flight_count > 0:
            print(f"The destination is currently used in {flight_count} flights and cannot be deleted")
            return

#if the destination can be deleted, the user is asked to confirm this. 
        print(f"Found destination: {destination[1]} ({iata_code})")  
        confirm = input(f"Are you sure you want to delete {iata_code}? (Y/N): ").strip().upper()

        if confirm != 'Y':
            print("Deletion cancelled.")
            return
        
#the destination is deleted. If there are any errors and the deletion cannot go ahead, messages appear. 
        try:
            self.cursor.execute("""
                DELETE FROM airport 
                    WHERE iata_code = ?
                """, (iata_code,))
            self.conn.commit()
            print(f"Destination {iata_code} deleted successfully.")
        except sqlite3.IntegrityError:
            print("Error: Cannot delete. The destination is likely used in other records (e.g., flights).")
            self.conn.rollback()
        except sqlite3.Error as retry:
            print(f"Database error: {retry}")
            self.conn.rollback()


    def close(self):
            self.conn.close()
        
