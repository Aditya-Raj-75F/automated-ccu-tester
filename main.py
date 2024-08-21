#!/usr/bin/env python3
import log_service
import ccu_data_reader
import adb_utils
import apk_installer_service
import bug_28245_testrun
import basic_utilities   # to support logging messages to stream and file
from basic_utilities import logged_input

import os
import sys
import signal
import logging

cur_dir = os.curdir

# This method is used to handle abrupting the program using Ctrl+C or SIGTERM
# It stops the logging service and exits the program
def signal_handler(sig, frame):
    log_service.stop_logging()
    logging.debug("\nSignal Received. Aborting all operations and exiting the program...")
    sys.exit(0)

# Registering the signal handler for SIGINT and SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# This method is used to display the options available for testing
def show_test_options():
     logging.debug("1. Take Logs")
     logging.debug("2. Stop Logs")
     logging.debug("3. Install Apk")
     logging.debug("4. Start App")
     logging.debug("5. Take Bug Report")
     logging.debug("6. Fetch DB")
     logging.debug("7. Fetch Preferences")
     logging.debug("8. Read Databases")
     logging.debug("9. Start Test Run")
     logging.debug("10. Run Command")
     logging.debug("11. Exit")
     logging.debug("0. Use device serial number")
     logging.debug("-1. Don't use device serial number")   

# Main method to start the program
if __name__ == "__main__":
    # Check if the user has provided any command line arguments
    if len(sys.argv) > 1:
        try:
            # Check if the command is to execute an adb command
            if sys.argv[1] == '-x':
                logging.debug(sys.argv)
                adb_command = sys.argv[2:]
                # Check if the command is to install an apk
                # If yes, then call the run_install_command method to take logs, db, preferences and bugreport
                if all(keyword in adb_command for keyword in ['adb', 'install']):
                    # Extracts the serial number if provided by user in case of multiple devices
                    serial_number = sys.argv[4] if "-s" in adb_command else None
                    bug_28245_testrun.run_install_command(serial_number, adb_command)
                elif adb_command != '':
                    logging.debug("Executing command...")
                    adb_utils.execute_adb_command(adb_command)
                else:
                    logging.debug("Please provide a valid command")
        except Exception as e:
            logging.debug(f"Error while executing command: {e}")
    # If no command line arguments are provided, then start the menu driven program
    # Some of the options are not correctly implemented        
    else:
        logging.debug("Starting menu driven program...")             
        serial_number = None
        while True:
            logging.debug("Please choose the type of testing you want to do...")
            show_test_options()
            try:
                choice = int(logged_input("Enter your choice: "))
                if choice == 1:
                    log_service.start_logging(serial_number, cur_dir)
                elif choice == 2:
                    log_service.stop_logging()
                elif choice == 3:
                    logging.debug("Updating the CCU with 2.15.0 apk containing custom logs")
                    isDowngrade = True if logged_input("Is Downgrade required? Press Y to continue or any other key to skip: ").upper() == 'Y' else False
                    apk_installer_service.install_apk(serial_number, cur_dir + "/RENATUS_CCU_dev_qa_2.15.0.apk", isDowngrade)
                elif choice == 4:
                    logging.debug("Starting the application...")
                    adb_utils.start_app(serial_number)
                elif choice == 5:
                    logging.debug("Taking bug report...")
                    adb_utils.take_bugreport(serial_number)
                elif choice == 6:
                    logging.debug("Fetching DB...")
                    adb_utils.fetch_db(serial_number)
                elif choice == 7:
                    logging.debug("Fetching preferences...")
                    adb_utils.fetch_preferences(serial_number)
                elif choice == 8:
                    logging.debug("Reading databases...")
                    logging.debug(ccu_data_reader.read_db(logged_input("Enter the path of the db: ")))
                elif choice == 9:
                    apk_path = logged_input("Enter the path of the apk to be installed:")
                    logging.debug(apk_path)
                    logging.debug("Starting test run...")
                    bug_28245_testrun.schedule_operations(serial_number, apk_path)
                elif choice == 10:
                    logging.debug("Running command...")
                    adb_utils.execute_adb_command(logged_input("Enter the command: "))
                elif choice == 11:
                    logging.debug("Exiting the program...")
                    sys.exit(0)
                elif choice == 0:
                    logging.debug("Using serial number of device for adb command.")
                    serial_number = logged_input("Please share the serial number here:")
                elif choice == -1:
                    logging.debug("Not using serial number of device for adb command.")
                    serial_number = None
                else:
                    logging.debug("Please choose among the valid options.")    
            except ValueError:
                logging.debug("Please enter a valid choice")    