

The files / folders that are used are as follows: 

•	main.py – entry point of system for the user 
•	Data folder: a folder created for all CSV files holding initial data. 
•	tables.ipynb:  a file used to create tables and insert initial data
•	flight_system_cli.py: runs the command-line interface (CLI)
•	flight_manager.py: handles flights
•	destination_manager.py: manages destinations
•	pilot_information.py: displays pilot data, including schedules
•	aircraft.py: manages aircraft 
•	analytics.py – produces reports

The Flight Management System 

The flight system is designed to manage and organize aspects of flight operations. It stores and links information about airports, aircraft, pilots, and flights, allowing for efficient scheduling, tracking, and assignment. The system handles:
•	Storing, adding, updating and deleting airport details to define flight origins and destinations
•	Managing aircraft data to assign specific planes to flights, including adding, updating and deleting redundant aircraft.
•	Keeping pilot records and linking them to flights. 
•	Providing pilot schedules
•	Scheduling, updating, and deleting flights
•	Ensuring data consistency and accuracy through relational connections between tables
•	Providing reports with analytics on flights and pilot workload. 
Overall, the system provides a structured and reliable way to coordinate flights, pilots, aircraft and airports. 

Useful information: 

pip install tabulate
pip install matplotlib



