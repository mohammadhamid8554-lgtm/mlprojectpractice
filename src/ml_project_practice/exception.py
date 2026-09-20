def error_message_detail(error, error_details):
    """Build a readable error message with traceback details."""
    # exc_info() gives us the traceback from the exception currently being handled.
    _, _, exc_tb = error_details.exc_info()

    if exc_tb is None:
        return str(error)

    # Include the file and line that caused the original failure.
    file_name = exc_tb.tb_frame.f_code.co_filename
    return (
        f"Error occurred in Python script [{file_name}] "
        f"at line {exc_tb.tb_lineno}: {error}"
    )

class CustomException(Exception):
    """Exception that keeps the original error plus useful traceback details."""

    def __init__(self, error, error_details):
        self.error_message = error_message_detail(error, error_details)
        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message