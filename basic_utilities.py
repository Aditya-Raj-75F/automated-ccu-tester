import logging
import datetime

output_filename = f"ccu-tester-output-log-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

# Set up logging to file and console
logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        handlers=[logging.FileHandler(output_filename, 'w', 'utf-8'), logging.StreamHandler()])

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)} hour(s), {int(minutes)} minute(s), and {int(seconds)} second(s)"
    elif minutes > 0:
        return f"{int(minutes)} minute(s) and {int(seconds)} second(s)"
    else:
        return f"{seconds:.2f} second(s)"

# input() method's wrapper Function to log input message and user input
def logged_input(prompt):
    logging.debug(prompt)
    user_input = input(prompt)
    logging.debug(f"user_response: {user_input}")
    return user_input