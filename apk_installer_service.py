from adb_utils import generate_adb_command
import basic_utilities   # to support logging messages to stream and file

import subprocess
import logging

def install_apk(serial_number, apk_path, downgrade=False):
    try:
        install_commands = ["install", "-r", "-d", apk_path] if downgrade else ["install", "-r", apk_path]
        install_process = subprocess.run(generate_adb_command(serial_number, install_commands), capture_output=True, text=True)
        if install_process.returncode == 0:
            logging.debug(f"{apk_path} installed successfully")
        else:
            logging.debug(f"Error while installing {apk_path}: {install_process.stderr}")
        return install_process.returncode
    except Exception as e:
        logging.debug(f"Error while installing {apk_path}: {e}")
        return -1