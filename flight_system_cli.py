import sqlite3

from pilot_information import PilotInformation
from flight_manager import FlightManager 
from destination_manager import DestinationManager
from aircraft import AircraftManager
from analytics import Analytics

class FlightSystemCLI:
    def __init__(self):
        self.conn = sqlite3.connect("flights.db") 

#pass a connection to each management class 

        self.pilot_info = PilotInformation(self.conn)
        self.flight_manager = FlightManager(self.conn)
        self.destination_manager = DestinationManager(self.conn)
        self.aircraft_manager = AircraftManager(self.conn)
        self.analytics = Analytics(self.conn)
        

    def run(self):
        while True:
            print("\n=== Flight Management System ===")
            print("1. Destinations")
            print("2. Pilot Information")
            print("3. Flights")
            print("4. Aircraft")
            print("5. Analytics")
            print("6. Exit")

            choice = input("Select the number and press Enter: ")
            if choice == '1':
                self.destination_menu()
            elif choice == '2':
                self.pilot_menu()
            elif choice == '3':
                self.flights_menu()
            elif choice == '4':
                self.aircraft_menu()
            elif choice == '5':
                self.analytics_menu()
            elif choice == '6':
                print("Goodbye!")
                break
            else:
                print("Invalid. Please try again.")

#Destination submenu
    def destination_menu(self):
        while True:
            print("\n--- Destination Menu ---")
            print("1. View All Destinations")
            print("2. Add a New Destination")
            print("3. Update a Destination")
            print("4. Delete a Destination")
            print("5. Return to Main Menu")

            choice = input("Select the number and press Enter: ")
            if choice == '1':
                self.destination_manager.view_destination()
            elif choice == '2':
                self.destination_manager.add_destination()
            elif choice == '3':
                self.destination_manager.update_destination()
            elif choice == '4':
                self.destination_manager.delete_destination()
            elif choice == '4':
                print("on hold")
            elif choice == '5':
                break
            else:
                print("Invalid. Please try again.")


#Pilot submenu
    def pilot_menu(self):
         while True:
            print("\n--- Pilot Information Menu ---")
            print("1. Pilot Information")
            print("2. Pilot Schedule")
            print("3. Return to Main Menu")

            choice = input("Select the number and press Enter: ")
            if choice == '1':
                self.pilot_info.view_pilots()
            elif choice == '2':
                self.pilot_info.view_pilot_schedule()
            elif choice == '3':
                break
            else:
                print("Invalid. Please try again.")

#Flight submenu
    def flights_menu(self):
        while True:
            print("\n--- Flights Information Menu ---")
            print("1. Add New Flight")
            print("2. View Flights by Criteria")
            print("3. Update a Flight")
            print("4. Delete a Flight")
            print("5. Return to Flights Menu")

            choice = input("Select the number and press Enter: ")
            if choice == '1':
                self.flight_manager.add_new_flight()
            elif choice == '2':
                self.retrieve_flight()
            elif choice == '3':
                self.flight_manager.update_flight()
            elif choice == '4':
                self.flight_manager.delete_flight()
            elif choice == '5':
                print("Return to Flights Menu")
                break
            else:
                print("Invalid. Please try again.")

    def retrieve_flight(self):
        while True:
            print("\n--- Retrieve Flight ---")
            print("1. By Flight ID")
            print("2. By Date")
            print("3. By Status")
            print("4. Flight Records: Choose Columns to Display")
            print("5. Return to Flights Menu")

            choice = input("Choose a search method and press Enter: ").strip()

            if choice == '1':
                self.flight_manager.search_by_flight_id()
            elif choice == '2':
                self.flight_manager.search_by_date()
            elif choice == '3':
                self.flight_manager.search_by_status()
            elif choice == '4':
                self.flight_manager.view_flights()
            elif choice == '5':
                break
            else:
                print("Invalid. Please try again.")

#aircraft menu
    def aircraft_menu(self):
        while True:
                print("\n--- Aircraft ---")
                print("1. View Aircraft")
                print("2. Add Aircraft")
                print("3. Delete Aircraft")
                print("4. Return to Main Menu")

                choice = input("Choose a search method and press Enter: ").strip()

                if choice == '1':
                    self.aircraft_manager.view_aircraft()
                elif choice == '2':
                    self.aircraft_manager.add_aircraft()
                elif choice == '3':
                    self.aircraft_manager.delete_aircraft()
                elif choice == '4':
                    break
                else:
                    print("Invalid. Please try again.")

#analytics menu
    def analytics_menu(self):
        while True:
                print("\n--- Reports ---")
                print("1. Flight and Destination Report")
                print("2. Pilot Workload Report")
                print("3. Return to Main Menu")

                choice = input("Choose a search method and press Enter: ").strip()

                if choice == '1':
                    self.analytics.flight_report()
                elif choice == '2':
                    self.analytics.pilot_report()
                elif choice == '3':
                    break
                else:
                    print("Invalid. Please try again.")

    def close(self):
        self.conn.close()

  
