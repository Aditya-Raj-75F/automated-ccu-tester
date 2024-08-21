from adb_utils import generate_adb_command
import basic_utilities  # to support logging messages to stream and file

import datetime
import subprocess
import threading
import logging

continue_logging = False

# Creates file path based on timestamp
def generate_log_file(path):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filepath = path + f'/log_{timestamp}.txt'
    return log_filepath

# Captures adb logs
def capture_logs(log_filename, serial_number):
    global continue_logging
    log_process = None
    try:
        with open(log_filename, "w", encoding="utf-8") as log_file:
            log_process = subprocess.Popen(
                generate_adb_command(serial_number, ["logcat","-v","threadtime"]), 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True,
                encoding="utf-8",
                errors='replace'
                )
            while continue_logging:
                output = log_process.stdout.readline()
                if output:
                    log_file.write(output)
                    log_file.flush()
            log_process.terminate()
            logging.debug(f"\nLogs captured successfully in {log_filename}")
    except Exception as e:
        logging.debug(f"Error while logging: {e}")
        if log_process:
            log_process.terminate()

# Starts logging on a separate thread
def start_logging(serial_number, path="."):
    global continue_logging
    continue_logging = True
    log_file_name = generate_log_file(path)
    logging.debug("Initiating android log capture...")
    threading.Thread(target=capture_logs, args=(log_file_name, serial_number,), name=log_file_name).start()
 
# Indicates to discontinue the logging operation    
def stop_logging():
    global continue_logging
    continue_logging = False
    logging.debug("Stopping android log capture...")