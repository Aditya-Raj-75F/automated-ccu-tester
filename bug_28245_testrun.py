import log_service
import apk_installer_service
import adb_utils
import ccu_data_reader
import basic_utilities   # to support logging messages to stream and file and other utilities

import os
import time
import datetime
import logging

continue_scheduling = False
count = 0
operation_dir_path = ""
preinstall_path = ""
postinstall_path = ""
post_app_start_10_path = ""
post_app_start_30_path = ""

cur_dir = os.curdir

#  This method is used to analyze the database for tables
#  If tables are cleared out, then it stops the operation and generates a bug report
def analyze_db(serial_number, db_path, event_message):
    global count, continue_scheduling
    logging.debug(f"Analyzing the database for tables... in db_path: {db_path}")
    tables_count = ccu_data_reader.read_db(db_path)
    if(tables_count['entities']==0 and tables_count['messages']==0 and tables_count['writable_array']==0):
        continue_scheduling = False
        logging.debug(event_message)
        logging.debug(f"Issue got replicated after {count} attempts. Stopping the operation.")
        count = 0
        log_service.stop_logging()
        logging.debug("Generating bug report...")
        adb_utils.take_bugreport(serial_number, operation_dir_path)
    else:
        logging.debug("Tables found in the database with the following counts:")
        logging.debug(f"Entities: {tables_count['entities']}, Messages: {tables_count['messages']}, WritableArray: {tables_count['writable_array']}")

# This method is used to start the operation
# It installs the apk, starts the app, fetches the ccu data and analyzes the database
def start_operation(serial_number, type="predefined", cmd=None, apk_path=None):
    global continue_scheduling, count, operation_dir_path, preinstall_path, postinstall_path, post_app_start_10_path, post_app_start_30_path
    log_service.start_logging(serial_number, operation_dir_path)
    adb_utils.fetch_ccu_data(serial_number, preinstall_path)
    count+=1
    continue_op = 0
    if type == "user-driven":
        continue_op = adb_utils.execute_adb_command(cmd)
    else:
        continue_op = apk_installer_service.install_apk(serial_number, apk_path)
    if continue_op != 0:
        logging.debug("Aborting the operation, since the app installation failed.")  
        log_service.stop_logging()
        return 
    logging.debug("Fetching the ccu data after the app installation...")
    adb_utils.fetch_ccu_data(serial_number, postinstall_path)
    analyze_db(serial_number, postinstall_path+"/databases", "No tables found in the database after install.")
    adb_utils.start_app(serial_number)
    time.sleep(10)
    logging.debug("Fetching the ccu data, 10 seconds after the app was started...")
    adb_utils.fetch_ccu_data(serial_number, post_app_start_10_path)
    analyze_db(serial_number, post_app_start_10_path+"/databases", "No tables found in the database, 10 seconds after the app was started.")  
    time.sleep(20)
    logging.debug("Fetching the ccu data, 30 seconds after the app was started...")
    adb_utils.fetch_ccu_data(serial_number, post_app_start_30_path)
    analyze_db(serial_number, post_app_start_30_path+"/databases", "No tables found in the database, 30 seconds after the app was started.")    
    log_service.stop_logging()

def create_dir_structure(tracks_dir_path):
    global operation_dir_path, preinstall_path, postinstall_path, post_app_start_10_path, post_app_start_30_path
    operation_dir_path = tracks_dir_path + "/operation_" + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    preinstall_path = operation_dir_path + "/pre-install"
    postinstall_path = operation_dir_path + "/post-install"
    post_app_start_10_path = operation_dir_path + "/post-app-start-10"
    post_app_start_30_path = operation_dir_path + "/post-app-start-30"
    os.makedirs(preinstall_path, exist_ok=True)
    os.makedirs(postinstall_path, exist_ok=True)
    os.makedirs(post_app_start_10_path, exist_ok=True)
    os.makedirs(post_app_start_30_path, exist_ok=True)

# This method is used to schedule the operations for testing the bug 28245
def schedule_operations(serial_number, apk_path):
    logging.debug("scheduling test operation for every 5 minutes...")
    tracks_dir = cur_dir + "/tracks-"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.makedirs(tracks_dir, exist_ok=True)
    global continue_scheduling, count
    count = 0
    continue_scheduling = True
    while continue_scheduling:
        logging.debug(f"Initiating test operation for the {count + 1} time")
        create_dir_structure(tracks_dir)
        logging.debug(f"apk_path  =  {apk_path}")
        start_operation(serial_number= serial_number, apk_path= apk_path)
        time.sleep(300)
    logging.debug("Test operation scheduling has been stopped, since app data is not available.")
    
#######################################USER-DRIVEN OPERATION############################################

# This method is used to run the install command provided by the user
def run_install_command(serial_number, adb_command):
    start_time = time.time()
    logging.debug("Creating directory structure before starting the operation...")
    tracks_dir = cur_dir + "/tracks-"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    os.makedirs(tracks_dir, exist_ok=True)
    create_dir_structure(tracks_dir)
    logging.debug("Starting the operation...")
    start_operation(serial_number= serial_number, type= "user-driven", cmd= adb_command)
    end_time = time.time()
    logging.debug(f"Total Time elapsed:{basic_utilities.format_time(end_time-start_time)}")