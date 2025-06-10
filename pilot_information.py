
from tabulate import tabulate

class PilotInformation:
    def __init__(self, connection):
        self.conn = connection
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

#1. calls all pilot records, allowing user select columns
    def view_pilots(self):

# Rename all column headings into user-friendly titles 
        column_map = {
            "pilot_id": "Pilot ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "experience_years": "Experience (Years)",
            "date_of_birth": "Date of Birth",
            "nationality": "Nationality",
            "phone_number": "Phone Number",
            "email": "Email",
            "passport_number": "Passport Number",
            "license_number": "License Number",
            "first_line_of_address": "Address Line 1",
            "town_city": "Town/City",
            "country": "Country",
            "postcode": "Postcode",
            "county": "County",
            "work_eligibility": "Work Eligibility"
        }

        all_columns = list(column_map.keys())       # this is a list of actual database fields  (i.e. the keys)
        display_names = list(column_map.values())   # this is a list of what the user sees with user-friendly names (i.e. the values)

#Print a list of options for the user to select from
        print("\nAvailable Columns:")
        for i, name in enumerate(display_names, start=1): # enumerate allocates the index number starting from 1 and the user-friendly column name
            print(f"{i}. {name}")

# The user selects which columns should be shown in the table. 

    # User is asked for their selection from a list and this is stored. 

        selected = input(
            "\nEnter column numbers separated by commas (e.g., 1,3,4) or press Enter to show all: "
        ).strip() 

        # the selection is then processed
        if selected:  #if the user provides an answer(i.e. the field is not left null)
            # try block to catch errors 
            try:
                indices = [int(i.strip()) - 1 for i in selected.split(",")]  # convert input to indexes
                selected_columns = [all_columns[i] for i in indices if 0 <= i < len(all_columns)]  # looks up actual database column names

#if no valid columns are selected, an error is triggered. 
                if not selected_columns:
                    raise ValueError

                selected_labels = [column_map[col] for col in selected_columns]  #get user-friendly display names

            except (ValueError, IndexError): #catch any errors, such invalude values as out of range index errors. 
                print("\nInvalid input.")
                input("Press Enter to return to the Pilot Information Menu.")
                return  
                
        else:
          
            selected_columns = all_columns #if the user presses enter, show all actual database columns names
            selected_labels = display_names # show all user-friendly column labels 

# Build the SQL query with aliases for user-friendly headers

        user_selection = ", ".join(f"{col} AS '{column_map[col]}'" for col in selected_columns) #maps each database column 
        view_selectedcolumns = f"SELECT {user_selection} FROM pilot" #this line creates the final SQL statement that will be eventually used. 


        self.cursor.execute(view_selectedcolumns) #executes query 
        matching_records = self.cursor.fetchall() #retrieves the matching records from teh query 

        if matching_records:
#displays results in a grid with user-friendly headers
            print("\n--- Pilot Information ---")
            print(tabulate(matching_records, headers=selected_labels, tablefmt="grid"))
        else:
            print("No pilot records found.") #if there is a n invalid query, this error message is shown. 

#2. Pulls a schedule for a specific pilot
    def view_pilot_schedule(self):
        pilot_id = input("Enter Pilot ID to view schedule: ").strip()

        # Check if pilot exists
        self.cursor.execute("""
            SELECT first_name, last_name
            FROM pilot
            WHERE pilot_id = ?
        """, (pilot_id,))
        pilot = self.cursor.fetchone()

        if not pilot:
            print("Pilot not found.")
            return

        print(f"\n--- Flight Schedule for {pilot[0]} {pilot[1]} ---")

# Retrieve flight schedule
        self.cursor.execute("""
            SELECT flight.flight_id, flight.flight_date, flight.flight_time, flight.origin_id, flight.destination_id, flight.status
            FROM flight
            JOIN flight_pilot ON flight.flight_id = flight_pilot.flight_id
            WHERE flight_pilot.pilot_id = ?
            ORDER BY flight.flight_date, flight.flight_time
        """, (pilot_id,))
        schedule = self.cursor.fetchall()

        if schedule:
            from tabulate import tabulate
            headers = ["Flight ID", "Date", "Time", "Origin", "Destination", "Status"]
            print(tabulate(schedule, headers=headers, tablefmt="grid"))
        else:
            print("No scheduled flights found for this pilot.")

    def close(self):
        self.conn.close()

