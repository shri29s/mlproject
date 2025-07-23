import sys
from src.logger import logging

def error_message_detail(error_message):
    _, _, error_tb = sys.exc_info()

    file_name = error_tb.tb_frame.f_code.co_filename
    line_no = error_tb.tb_lineno

    error_message = f"Error occurred in python script name [{file_name}] line number [{line_no}] with error message [{str(error_message)}]"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message)
        logging.error(self.error_message)

    def __str__(self):
        return self.error_message
    
# if __name__=="__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         print(CustomException("Cannot divide by zero"))