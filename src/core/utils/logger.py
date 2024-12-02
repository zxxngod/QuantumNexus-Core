import logging
import os

class Logger:
    def __init__(self, name, log_file='app.log', level=logging.INFO):
        """Initialize the logger with a specified name, log file, and logging level."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a file handler
        if not os.path.exists('logs'):
            os.makedirs('logs')
        file_handler = logging.FileHandler(os.path.join('logs', log_file))
        file_handler.setLevel(level)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create a formatter and set it for both handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """Return the logger instance."""
        return self.logger

# Example usage
if __name__ == "__main__":
    logger = Logger(__name__).get_logger()
    logger.info("Logger initialized.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
