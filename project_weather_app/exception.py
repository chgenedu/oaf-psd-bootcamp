# Some custom exceptions for this project

class ModeError(Exception):
    def __init__(self, message, mode, error_code):
        super().__init__(message)
        self.error_code = error_code
        print(message)
        print("Mode: ", mode)
        print("Error code: ", self.error_code)
        exit(self.error_code)
