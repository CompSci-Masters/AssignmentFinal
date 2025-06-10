import matplotlib.pyplot as plt  

import matplotlib
matplotlib.use('Agg')  

class Analytics:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

    # 1. Creates a report with useful graphs
    def flight_report(self):
        print("\n--- Flight and Destination Report ---")  
        fig, chart_details = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Flight and Destination Report", fontsize=16)

        # a. Total Number of Flights 
        self.cursor.execute("""SELECT COUNT(*) FROM flight""")
        total_flights = self.cursor.fetchone()[0]

        chart_details[1, 1].axis('off')
        chart_details[1, 1].text(0.1, 0.6, f"Total Flights: {total_flights}", fontsize=14)

        # b. Flights by Status
        self.cursor.execute("""
            SELECT status, COUNT(*) 
            FROM flight 
            GROUP BY status
        """)
        status_information = self.cursor.fetchall()
        if status_information:
            statuses, status_count = zip(*status_information)
            chart_details[0, 0].bar(statuses, status_count)
            chart_details[0, 0].set_title("Flights by Status")
            chart_details[0, 0].set_xlabel("Status")
            chart_details[0, 0].set_ylabel("Count")

        # c. Flights per Day
        self.cursor.execute("""
            SELECT flight_date, COUNT(*) 
            FROM flight
            GROUP BY flight_date 
            ORDER BY flight_date
        """)
        flight_dates = self.cursor.fetchall()
        if flight_dates:
            dates, flight_counts = zip(*flight_dates)
            chart_details[0, 1].plot(dates, flight_counts, marker='o')
            chart_details[0, 1].set_title("Flights per Day")
            chart_details[0, 1].set_xlabel("Date")
            chart_details[0, 1].set_ylabel("Number of Flights")
            chart_details[0, 1].tick_params(axis='x', rotation=45)

        # d. Top 5 Routes
        self.cursor.execute("""
            SELECT origin_id || ' to ' || destination_id AS route, COUNT(*) AS count
            FROM flight
            GROUP BY origin_id, destination_id
            ORDER BY count DESC
            LIMIT 5
        """)
        route_information = self.cursor.fetchall()
        if route_information:
            route, route_count = zip(*route_information)
            chart_details[1, 0].barh(route, route_count)
            chart_details[1, 0].set_title("Top 5 Routes")
            chart_details[1, 0].set_xlabel("Flights")
            chart_details[1, 0].invert_yaxis()

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        fig.savefig("flight_report.png")  
        print("Flight report saved as 'flight_report.png'")  

    # 2. Pilot Workload Report
    def pilot_report(self):
        print("\n--- Pilot Workload Report ---")  

        self.cursor.execute("""
            SELECT pilot.pilot_id, pilot.last_name, COUNT(*) AS flight_count
            FROM flight_pilot
            JOIN pilot ON flight_pilot.pilot_id = pilot.pilot_id
            GROUP BY pilot.pilot_id, pilot.last_name
        """)
        pilot_details = self.cursor.fetchall()

        if not pilot_details:
            print("No pilot_details available.")
            return

        graph_label = [f"{pilot} {lastname}" for pilot, lastname, _ in pilot_details]
        counts = [count for _, _, count in pilot_details]

        plt.figure(figsize=(10, 6))
        plt.bar(graph_label, counts)
        plt.title("Flights per Pilot")
        plt.xlabel("Pilot ID & Last Name")
        plt.ylabel("Number of Flights")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig("pilot_report.png")  
        print("Pilot report saved as 'pilot_report.png'")  

    def close(self):
        self.conn.close()
