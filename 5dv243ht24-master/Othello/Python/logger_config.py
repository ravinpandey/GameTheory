import logging

# Create a logger instance
logger = logging.getLogger()

# Set the logging level
logger.setLevel(logging.INFO)

# Create file handler which logs to 'game_log.txt'
file_handler = logging.FileHandler('game_log.txt')
file_handler.setLevel(logging.INFO)

# Create console handler which logs to console (stdout)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Now, the logger will write to both the file and the console

