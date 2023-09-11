import os
import sys
import logging
import datetime

LOG_FILE = os.getenv("LOG_FILE")
LOG_FILE = f"{LOG_FILE}FIS-Service-{datetime.datetime.now():%Y_%m}.log"

class Logger:
    def __init__(self, log_file_path: str = LOG_FILE):
        """
        Initializes the logger object with necessary parameters.
        """
        try:
            os.remove(path=LOG_FILE) 
        except:
            pass
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        
        # Create file handler if log file path exists
        if log_file_path:
            self.file_handler = logging.FileHandler(log_file_path)
            self.file_handler.setLevel(logging.DEBUG)
            self.file_handler.setFormatter(self.formatter)
            self.logger.addHandler(self.file_handler)
        
        self.stdout_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stdout_handler)

    def log_message(self, message: str, log_level: str):
        """
        Logs the provided message with given log level.
        """
        if log_level not in ["info", "error", "warning", "debug"]:
            raise ValueError("Invalid log level")

        if log_level == "info":
            self.logger.info(message)
        elif log_level == "error":
            self.logger.error(message)
        elif log_level == "warning":
            self.logger.warning(message)
        elif log_level == "debug":
            self.logger.debug(message)


# if __name__ == '__main__':
    # Example usage
    # LOGFILE = os.getenv('SER_LOG') + f"ncsc_{datetime.datetime.now():%Y_%m}.log"
    # logger = Logger(LOGFILE)  # Remove parameter here to disable file logging
    # logger.log_message("test log info", "info")
