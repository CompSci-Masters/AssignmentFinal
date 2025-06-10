import sqlite3
from tabulate import tabulate  

class AircraftManager:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

#view a list of aircraft
    def view_aircraft(self):
        try:
            self.cursor.execute("""
                SELECT aircraft_id, model, capacity, manufacturer, registration_number
                FROM aircraft
            """)
            aircraft = self.cursor.fetchall()

            if aircraft:
                print("\n--- Aircraft List ---")
                print(tabulate(aircraft, headers=["Aircraft ID", "Model", "Capacity", "Manufacturer", "Registration_number"], tablefmt="grid"))
            else:
                print("No aircraft records found.")

        except sqlite3.Error as e:
            print(f"Error retrieving aircraft data: {e}")

#add a new aircraft
    def add_aircraft(self):
        print("\n--- Add New Aircraft ---")
        
# Get aircraft details from the user
        aircraft_id = input("Enter Aircraft ID: ").strip()
        model = input("Enter Aircraft Model: ").strip()
        capacity = input("Enter Capacity: ").strip()
        manufacturer = input("Enter Manufacturer: ").strip()
        registration_number = input("Registration Number: ").strip()

# Insert the new aircraft into the database
        try:
            self.cursor.execute("""
                INSERT INTO aircraft (aircraft_id, model, capacity, manufacturer, registration_number)
                VALUES (?, ?, ?, ?, ?)
            """, (aircraft_id, model, capacity, manufacturer, registration_number))
            self.conn.commit()
            print("Aircraft added successfully.")
        except sqlite3.IntegrityError:
            print("Error: Aircraft ID already exists.")
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Failed to add aircraft: {e}")

#delete an aircraft, as long as it is not allocated to an existing flight
    def delete_aircraft(self):
        print("\n--- Delete Aircraft ---")
        aircraft_id = input("Enter Aircraft ID to delete: ").strip()

# Check if the aircraft exists
        self.cursor.execute("SELECT * FROM aircraft WHERE aircraft_id = ?", (aircraft_id,))
        record = self.cursor.fetchone()

        if not record:
            print("Aircraft not found.")
            return

# Confirm deletion
        confirm = input(f"Are you sure you want to delete aircraft '{aircraft_id}'? (Y/N): ").strip().upper()
        if confirm != 'Y':
            print("Deletion cancelled.")
            return

        try:
            self.cursor.execute("DELETE FROM aircraft WHERE aircraft_id = ?", (aircraft_id,))
            self.conn.commit()
            print("Aircraft deleted successfully.")
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Failed to delete aircraft: aircraft may be allocated to existing flights")

    def close(self):
        self.conn.close()
