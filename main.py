
from flight_system_cli import FlightSystemCLI

# This Class creates an app object that initializes and runs the FlightSystemCLI class, starting the menu system when the script is executed directly.
class MainApp:
    def __init__(self):
        self.cli = FlightSystemCLI()

    def run(self):
        self.cli.run()

if __name__ == "__main__":
    app = MainApp()
    app.run()