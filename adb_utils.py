import basic_utilities  # to support logging messages to stream and file

import subprocess
import logging

def execute_adb_command(adb_command):
    try:
        process = subprocess.run(adb_command, shell=True, text=True)
        if process.returncode == 0:
            logging.debug(f"Command executed successfully: {adb_command}")
        else:
            logging.debug(f"Error while executing command: {process.stderr}")
        return process.returncode
    except Exception as e:
        logging.debug(f"Unhandled Exception: Error while executing command: {e}")
        return -1

def generate_adb_command(serial_number, command):
    adb_command = ["adb"] if serial_number is None else ["adb", "-s", serial_number]
    adb_command.extend(command)
    return adb_command

def take_bugreport(serial_number, path="."):
    try:
        bugreport_process = subprocess.run(generate_adb_command(serial_number, ["bugreport", path]), capture_output=True, text=True)
        if bugreport_process.returncode == 0:
            logging.debug("Bugreport captured successfully")
        else:
            logging.debug(f"Error while capturing bugreport: {bugreport_process.stderr}")
    except Exception as e:
        logging.debug(f"Error while capturing bugreport: {e}")

def start_app(serial_number):
    try:
        start_app_process = subprocess.run(generate_adb_command(serial_number, ["shell", "am", "start", "-n", "a75f.io.renatus/a75f.io.renatus.SplashActivity"])
                                           , capture_output=True, text=True)
        if start_app_process.returncode == 0:
            logging.debug("App started successfully")
        else:
            logging.debug(f"Error while starting app: {start_app_process.stderr}")
    except Exception as e:
        logging.debug(f"Error while starting app: {e}")

def fetch_db(serial_number, path="."):
    try:
        fetch_db_process = subprocess.run(generate_adb_command(serial_number, ["pull", "/data/data/a75f.io.renatus/databases", path]), capture_output=True, text=True)
        if fetch_db_process.returncode == 0:
            logging.debug(f"DB fetched successfully to path: {path}")
        else:
            logging.debug(f"Error while fetching DB: {fetch_db_process.stderr} to path: {path}")
    except Exception as e:
        logging.debug(f"Exception: Error while fetching DB: {e}")

def fetch_preferences(serial_number, path="."):
    try:
        fetch_preferences_process = subprocess.run(generate_adb_command(serial_number, ["pull", "/data/data/a75f.io.renatus/shared_prefs", path]), capture_output=True, text=True)
        if fetch_preferences_process.returncode == 0:
            logging.debug(f"Preferences fetched successfully to path {path}")
        else:
            logging.debug(f"Error while fetching preferences: {fetch_preferences_process.stderr} to path: {path}")
    except Exception as e:
        logging.debug(f"Exception: Error while fetching preferences: {e}")

def fetch_ccu_data(serial_number, path="."):
    fetch_db(serial_number, path)
    fetch_preferences(serial_number, path)