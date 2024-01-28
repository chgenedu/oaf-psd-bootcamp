# Some custom exceptions for this project
import logging
logger = logging.getLogger(__name__)

MODE_ERROR_EXIT_CODE = 2
CONFIG_FILE_ERROR_EXIT_CODE = 2
DATABASE_ERROR_EXIT_CODE = 2
DATA_SERVICE_ERROR_EXIT_CODE = 2

class ModeError(Exception):
    def __init__(self, message, mode):
        """
        This exception is for selecting an invalid mode for the program.
        """
        super().__init__(message)
        self.exit_code = MODE_ERROR_EXIT_CODE
        logger.error(message)
        logger.error("Mode: " + str(mode))
        exit(self.exit_code)

class ConfigFileError(Exception):
    def __init__(self, message, filepath, exception_error=Exception):
        """
        This exception is for problems related to the config file.
        """
        super().__init__(message)
        self.exit_code = CONFIG_FILE_ERROR_EXIT_CODE
        logger.error(message)
        logger.error("Exception: " + str(exception_error))
        logger.error("ConfigFile: " + str(filepath))        
        exit(self.exit_code)

class DatabaseError(Exception):
    def __init__(self, message, exception_error=Exception):
        """
        This exception is for any issues related to database access.
        """
        super().__init__(message)
        self.exit_code = DATABASE_ERROR_EXIT_CODE
        logger.error(message)
        logger.error("Exception: " + str(exception_error))
        exit(self.exit_code)

class DataServiceError(Exception):
    def __init__(self, message, exception_error=Exception):
        """
        This exception is for any issues related to getting data service.
        """
        super().__init__(message)
        self.exit_code = DATA_SERVICE_ERROR_EXIT_CODE
        logger.error(message)
        logger.error("Exception: " + str(exception_error))
        exit(self.exit_code)
