import sqlite3
from tabulate import tabulate
from datetime import datetime

class FlightManager:
    def __init__(self, connection):
        self.conn = connection
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()


    #allow the user to view flight by flight ID
    def search_by_flight_id(self):
        flight_id = input("Enter Flight ID: ").strip()
        self.cursor.execute("""
            SELECT flight_id, origin_id, destination_id, flight_date, flight_time, status
            FROM flight WHERE flight_id = ?
        """, (flight_id,))
        result = self.cursor.fetchone()
        if result:
            print("\nFlight Found:")
            print(tabulate([result], headers=["ID", "Origin", "Destination", "Date", "Time", "Status"], tablefmt="pretty"))
        else:
            print("No flight found with that ID.")

    def search_by_date(self):
        search_date = input("Enter flight start date for the period you wish to view (DD/MM/YYYY): ").strip()

#check that the date is in the correct format. 
        try:
            datetime.strptime(search_date, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format. Please enter as DD/MM/YYYY.")
            return
                
#find flights with that date and order the table by flight_id. 
        self.cursor.execute("""
            SELECT flight_id, origin_id, destination_id, flight_date, flight_time, status
            FROM flight
            WHERE flight_date = ?
            ORDER BY flight_time
            """, (search_date,))
        
#create a table with the flights on the provided date.         
        results = self.cursor.fetchall()
        if results:
            print(f"\nFlights on {search_date}:")
            print(tabulate(results, headers=["ID", "Origin", "Destination", "Date", "Time", "Status"], tablefmt="pretty"))
        else:
            print("No flights found on that date.")

    def search_by_status(self):

        status_options = {
        "1": "Scheduled",
        "2": "Delayed",
        "3": "Cancelled"
        }

        print("\nSearch by Flight Status:")

        for status_number, status in status_options.items():
            print(f"{status_number}. {status}")

        choice = input("Enter your choice (1 / 2 / 3): ").strip()

        if choice not in status_options:
            print("Invalid status choice. Please enter 1, 2, or 3.")
            return

        selected_status = status_options[choice]

        self.cursor.execute("""
            SELECT flight_id, origin_id, destination_id, flight_date, flight_time, status
            FROM flight
                WHERE status = ?
                ORDER BY flight_date, flight_time
        """, (selected_status,))

        results = self.cursor.fetchall()
        if results:
            print(f"\nFlights with status '{selected_status}':")
            print(tabulate(results, headers=["Flight ID", "Origin", "Destination", "Date", "Time", "Status"], tablefmt="pretty"))
        else:
            print(f"No flights found with status '{selected_status}'.")







#calls all flights, allowing user to filter by column heading. This includes flight information and pilot information. 
    def view_flights(self):
# Rename all column headings into user-friendly titles 
        column_map = {
            "flight.flight_id": "Flight ID",
            "flight.origin_id": "Origin Airport",
            "flight.destination_id": "Destination Airport",
            "flight.aircraft_id": "Aircraft ID",
            "flight.flight_date": "Date",
            "flight.flight_time": "Time",
            "flight.status": "Status",
            "pilot.pilot_id": "Pilot ID",
            "pilot.first_name": "Pilot First Name",
            "pilot.last_name": "Pilot Last Name"        

        }

        all_columns = list(column_map.keys()) #stores the actual database column names (i.e. the keys)
        display_names = list(column_map.values()) #stores the names to be displayed (i.e. the values)

#Print a list of options for the user to select from. 
        print("\nAvailable Columns:")
        for i, name in enumerate(display_names, start=1): #enumerate allocates index number starting from 1 followed by the user-friendly column name 
            print(f"{i}. {name}")


# The user selects which columns should be shown in the table. 

    # User is asked for their selection from a list and this is stored. 

        selected = input("\nEnter column numbers separated by commas (e.g., 1,3,4) or press Enter to show all: ").strip()

        if selected: #if the user provides an answer(i.e. the field is not left null)
            try:
                indices = [int(i.strip()) - 1 for i in selected.split(",")] #this converts the input into indicies 
                selected_columns = [all_columns[i] for i in indices if 0 <= i < len(all_columns)] # the actual database column names are looked up

                if not selected_columns: #if no valid columns are selected, an error is triggered. 
                    raise ValueError

                selected_labels = [column_map[col] for col in selected_columns] #get user-friendly display names
            except (ValueError, IndexError): #catch any errors, such as out of range index errors. 

                print("\nInvalid input.")
                return
        else:
            selected_columns = all_columns #if the user presses enter, show all actual database columns names
            selected_labels = display_names # show all user-friendly column labels 

        # Build the SQL query with aliases for user-friendly headers
        select_clause = ", ".join(f"{col} AS '{column_map[col]}'" for col in selected_columns) #maps each database column 

        #this creates the final SQL statement tha will be eventually used. 
        view_query = f"""
            SELECT {select_clause} 
            FROM flight
            LEFT JOIN flight_pilot ON flight.flight_id = flight_pilot.flight_id
            LEFT JOIN pilot ON flight_pilot.pilot_id = pilot.pilot_id
        """

        try:
            self.cursor.execute(view_query) #executes query 
            matching_records = self.cursor.fetchall() #retrieves the matching records from teh query 

            if matching_records:
            #displays results in a grid with user-friendly headers
                print("\n--- Flight Information ---")
                print(tabulate(matching_records, headers=selected_labels, tablefmt="grid"))

            else:
                print("No flight records found.")
        except sqlite3.Error as e:
            print(f"Unable to fetch flight data. Please try again.: {e}") #if there is a n invalid query, this error message is shown. 
            






    def add_new_flight(self):
        print("\n=== Add New Flight ===")

    # Get and validate origin airport
        origin_id = input("Enter origin IATA code: ").upper()
        self.cursor.execute("""
            SELECT name 
            FROM Airport
                WHERE iata_code = ?
        """, (origin_id,))
        if not self.cursor.fetchone():
            print("Origin IATA code not found in records.")
            return

        # Get and validate destination airport
        destination_id = input("Enter destination IATA code: ").upper()
        self.cursor.execute("""
            SELECT name 
            FROM airport 
                WHERE iata_code = ?
        """, (destination_id,))
        if not self.cursor.fetchone():
            print("Destination IATA code not found in records.")
            return


        # Get departure datetime
        date_input = input("Enter departure date (DD/MM/YYYY): ")
        flight_time = input("Enter departure time (HH:MM in 24h format): ")
        try:
            datetime.strptime(date_input, "%d/%m/%Y")  # checks the date is formatted correctly 
            datetime.strptime(flight_time, "%H:%M")  #checks the time is formatted correctly 
        except ValueError:
            print("Invalid date/time format.")
            return

        # Get flight status
        status_options = {
            "1": "Scheduled",
            "2": "Delayed",
            "3": "Cancelled"
        }

        print("Select flight status")
        for selected_number, selected_status in status_options.items():
            print(f"{selected_number}. {selected_status}")

        status_choice = input("Enter choice (1 / 2 / 3)").strip()

        if status_choice not in status_options:
            print("Invalid. Please enter either 1 / 2 / 3")
            return
        
        status = status_options[status_choice]
    

        # Ask if user wants to view pilot list
        view_pilots = input("Would you like to see a list of available pilots? (Y/N): ").strip().upper()
        
        if view_pilots == 'Y':
        # This code identifies any pilots with flights on the date requested. These pilots are removed from the list.    
        # This first lists the pilots who currently have flights on the date provided by the user.     

            self.cursor.execute("""
                SELECT flight.flight_id, flight_pilot.pilot_id, flight.flight_time
                FROM flight_pilot
                JOIN flight ON flight_pilot.flight_id = flight.flight_id
                WHERE flight.flight_date = ?
                """, (date_input,))

            day_flights = self.cursor.fetchall()
            print("Flights found on that day:")
            if day_flights:
                print("Flights found on this date")
                print(tabulate(day_flights, headers=["Flight Number", "Pilot ID", "Flight Time"], tablefmt="pretty"))
            else:
                print("There are no flights currently scheduled on this date.")

        # Secondly a list shows the pilots are available for the flight on this date.
            self.cursor.execute("""
                SELECT pilot_id, first_name, last_name
                FROM pilot
                WHERE pilot_id NOT IN (
                    SELECT pilot_id
                    FROM flight_pilot
                    JOIN flight ON flight_pilot.flight_id = flight.flight_id
                     WHERE flight.flight_date  = ?          
                )
                """, (date_input,))

            pilots = self.cursor.fetchall()
            if pilots:
                print("\nAvailable Pilots:")
                print(tabulate(pilots, headers=["Pilot ID", "First Name", "Last Name"], tablefmt="pretty"))
            else:
                print("No pilots found in the system.")
                return
            
               # Get pilot ID. Always ask for the pilot_id, regardless of whether the user views the list or not. 
        pilot_id = input("Enter  pilot ID to assign to flight: ").strip()
        self.cursor.execute("SELECT first_name, last_name FROM Pilot WHERE pilot_id = ?", (pilot_id,))
        pilot = self.cursor.fetchone()
        if not pilot:
            print("Pilot ID not found in records.")
            return
        
         # Get aircraft ID
        #reqeust ID from the user. If it doesn't match an aircraft_id in the aircraft table, error message is returned. The User is asked to select a validated aircraft_ID from a list. 
        print("\n--- Available Aircraft ---")
       

    # Create a list of available aircraft for the user to choose from on the given date. If no aircraft are available, the user will be notified. Assumption:oOne flight per aircraft is available per day. 
        self.cursor.execute("""
            SELECT aircraft_id, registration_number, capacity, model
            FROM aircraft 
            WHERE aircraft_id NOT IN (
                SELECT aircraft_id
                FROM flight
                WHERE flight_date  = ?          
                )
            """, (date_input,)) 
        available_plane = self.cursor.fetchall()
# It may be that all aircraft are allocated to flights on the date provided. This catches them.
        if not available_plane:
            print("Either all aircraft are being used, or your selected aircraft is being used for another flight on this day. Please make another selection")
            input("Press enter to return to the menu")
            return None #This prevents the rest of the code from running
        
        for aircraft_id, registration_number, capacity, model in available_plane:
            print(f"{aircraft_id}: {registration_number} {capacity} {model}")

        aircraft_id = None #the user may select an invalid aircraft id. This initialises aircraft_id

        while True:
            try:
                selected_id = int(input("Enter the Aircraft ID you want to use: ").strip())
                self.cursor.execute("""
                    SELECT aircraft_id 
                    FROM aircraft 
                    WHERE aircraft_id = ?
                        AND aircraft_id NOT IN(
                            SELECT aircraft_id
                            FROM flight
                            WHERE flight_date = ?
                                    )
                """, (selected_id, date_input))
                if self.cursor.fetchone():
                    aircraft_id = selected_id
                    break
                else:
                    print("Invalid Aircraft ID. Please select from the list.")
            except ValueError:
                print("Please enter a valid numeric ID.")

        if aircraft_id is None:
            print("Aircraft number is invalid.")
            return

        # This try inserts data into the tables. Any errors result in a message. 
        try:
        # inserts new flight information into flight table
            self.cursor.execute("""
                INSERT INTO flight (origin_id, destination_id, aircraft_id, flight_date, flight_time, status) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (origin_id, destination_id, aircraft_id, date_input, flight_time, status)) 
            flight_id = self.cursor.lastrowid

        # inserts pilot infromation into pilot table

            self.cursor.execute("""
                INSERT INTO flight_pilot (flight_id, pilot_id)
                VALUES (?, ?)
            """, (flight_id, pilot_id))

            self.conn.commit()
            print(f"\nFlight {flight_id} added with pilot {pilot_id} ({pilot[0]} {pilot[1]}).")
            print(" Reminder: If this flight leaves Heathrow, please add the return flight now as we do not want pilots stranded overseas. Please ensure that the pilot has a sufficient break before the return flight. ")
            input("\nPlease press enter to return to the menu")

        except sqlite3.Error as e:
            print(f"Database rejection, please start again: {e}")
            self.conn.rollback()





    def update_flight(self):
        flight_id = input("Enter the Flight ID to update: ").strip()

        self.cursor.execute("""
            SELECT flight.*, pilot.pilot_id, pilot.first_name, pilot.last_name
            FROM flight
            LEFT JOIN flight_pilot ON flight.flight_id = flight_pilot.flight_id
            LEFT JOIN pilot ON flight_pilot.pilot_id = pilot.pilot_id
            WHERE flight.flight_id = ?
        """, (flight_id,))
        flight_data = self.cursor.fetchone()

        if not flight_data:
            print("Flight not found.")
            return

        print("\n--- Current Flight Details ---")
        print(f"Flight ID: {flight_data[0]} | Origin: {flight_data[1]} | Destination: {flight_data[2]} | Aircraft: {flight_data[3]} | Date: {flight_data[4]} | Time: {flight_data[5]} | Status: {flight_data[6]} | Pilot ID: {flight_data[7]} | First Name: {flight_data[8]} | Last Name {flight_data[9]}")

        # Ask for new details
        new_origin = input("Enter new Origin IATA code (or press Enter to keep current): ").strip().upper() or flight_data[1]
        new_destination = input("Enter new Destination IATA code (or press Enter to keep current): ").strip().upper() or flight_data[2]
        
        while True:
            new_aircraft_id = input("Enter new Aircraft ID (or press Enter to keep current): ").strip() or str(flight_data[3])

#Check if the selected aircraft is already scheduled for use on the same date
            self.cursor.execute("""
                SELECT COUNT(*) FROM flight
                WHERE aircraft_id = ? AND flight_date = ? AND flight_id != ?
            """, (new_aircraft_id, flight_data[4], flight_id))
            aircraft_conflict = self.cursor.fetchone()[0] > 0

            if aircraft_conflict:
                print("Aircraft conflict: This aircraft is already assigned to another flight on this date.")
            else:
                break 
            

        new_date = input("Enter new Flight Date (DD/MM/YYYY) (or press Enter to keep current): ").strip() or flight_data[4]
        new_time = input("Enter new Flight Time (HH:MM) (or press Enter to keep current): ").strip() or flight_data[5]
        new_status = input("Do you want to update the Status? (Y/N): ").strip().upper()
        
        if new_status == 'Y':        
            print("\nSelect a new flight status:")
            print("1. Scheduled")
            print("2. Delayed")
            print("3. Cancelled")

            status_choice = input("Enter choice 1 - 3: ").strip()
            status_map = {"1": "Scheduled", "2": "Delayed", "3": "Cancelled"}
            new_status = status_map.get(status_choice)

            if not new_status:
                print("Invalid status selection.")
                return
        else:
            new_status = flight_data[6]

        # Check if pilot update is needed
        change_pilot = input("Do you want to update the pilot? (Y/N): ").strip().upper()
        new_pilot_id = str(flight_data[7]) #set's default to existing pilot

        if change_pilot == 'Y':
            new_pilot_id = input("Enter new Pilot ID: ").strip()
            
#checks that the pilot exists in the database
            self.cursor.execute("""
                SELECT first_name, last_name 
                FROM pilot 
                WHERE pilot_id = ?
            """, (new_pilot_id,))
            pilot_record = self.cursor.fetchone()

            if not pilot_record:
                print("Pilot not found.")
                return
            
            
    

        # Checks that there are no conflict with pilot on same date

        if new_pilot_id:
            self.cursor.execute("""
                SELECT COUNT(*) 
                FROM flight_pilot
                JOIN flight ON flight.flight_id = flight_pilot.flight_id
                WHERE flight.flight_date = ? AND flight_pilot.pilot_id = ? AND flight.flight_id != ?
            """, (new_date, new_pilot_id, flight_id))
            conflict_pilot = self.cursor.fetchone()[0] > 0

            if conflict_pilot:
                print("This pilot is assigned to another flight on this date. Please see a list of available pilots below")
#provides a list of available pilots on this date
                self.cursor.execute("""
                    SELECT pilot_id, first_name, last_name 
                    FROM pilot
                    WHERE pilot_id NOT IN (
                        SELECT pilot_id 
                        FROM flight_pilot 
                        JOIN flight ON flight.flight_id = flight_pilot.flight_id 
                        WHERE flight.flight_date = ?
                    )
                """, (new_date,))
                available_pilots = self.cursor.fetchall()

                if available_pilots:
                    for pilot in available_pilots:
                        print(f"{pilot[0]}: {pilot[1]} {pilot[2]}")

                else:
                    print("No available pilots on this date.")
                    input("Press Enter to return to the menu.")

                while True:
                    new_pilot_id2 = input("Please enter a different Pilot ID from the list above: ").strip()

                    if not new_pilot_id2.isdigit():
                        print("Invalid input.")
                        continue

                    new_pilot_id2 = int(new_pilot_id2)

                    if any(pilot[0] == new_pilot_id2 for pilot in available_pilots):
                        new_pilot_id = new_pilot_id2
                        break
                    
                    else:
                        print("Invalid Pilot ID. Please choose one from the list.")
        else:
            print("No pilots available on this date. Please press enter to return to the menu.")
            input()
            return
                    
        # Update the flight record
        try:
            self.cursor.execute("""
                UPDATE flight
                SET origin_id = ?, destination_id = ?, aircraft_id = ?, flight_date = ?, flight_time = ?, status = ?
                WHERE flight_id = ?
            """, (new_origin, new_destination, new_aircraft_id, new_date, new_time, new_status, flight_id))

            if new_pilot_id:
                self.cursor.execute("""
                    DELETE FROM flight_pilot 
                    WHERE flight_id = ?
                """, (flight_id,))
                self.cursor.execute("""
                    INSERT INTO flight_pilot (flight_id, pilot_id) 
                    VALUES (?, ?)
                """, (flight_id, new_pilot_id))
                

            self.conn.commit()
            print("Flight updated successfully.")
            input("\nPlease press enter to return to the menu")

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Failed to update flight: {e}")


#delete flight requesting flight_id from the user 

    def delete_flight(self):
        flight_id = input("Enter the Flight ID to delete: ").strip()

        # Confirm the flight exists
        self.cursor.execute("""
            SELECT * FROM flight 
                WHERE flight_id = ?
            """, (flight_id,))
        flight = self.cursor.fetchone()

        if not flight:
            print("Flight not found.")
            return

        # Confirm deletion
        confirm = input(f"Are you sure you want to delete Flight ID {flight_id}? (Y/N): ").strip().upper()
        if confirm != 'Y':
            print("Deletion cancelled.")
            return

        try:
            # Delete related pilot assignment first (if any)
            self.cursor.execute("""
                DELETE FROM flight_pilot 
                    WHERE flight_id = ?
            """, (flight_id,))
            
            # Delete the flight record
            self.cursor.execute("""
                DELETE FROM flight
                    WHERE flight_id = ?
            """, (flight_id,))

            self.conn.commit()
            print(f"Flight ID {flight_id} deleted successfully.")

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Failed to delete flight: {e}")

    def close(self):
        self.conn.close()