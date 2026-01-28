# import sys 
# import traceback
# from logger.custom_logger import CustomLogger
# logger = CustomLogger().get_logger(__file__)

# class DocumentPortalException(Exception):
#     """ Custom Exception for Document Portal """
#     def __init__(self, error_message, error_details:sys):
#         print(error_details.exc_info())
#         _,_,exc_tb = error_details.exc_info() #exc_tb execution traceback, exc_info execution info ( the information that are not important
#         # will be kept in underscore as seen _,)
#         self.file_name = exc_tb.tb_frame.f_code.co_filename
#         self.lineno = exc_tb.tb_lineno
#         self.error_message = str(error_message)
#         self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info()))

#     def __str__(self):
#         return f"""
#         Error in [{self.file_name}] at line [{self.lineno}]
#         Message: {self.error_message}
#         Traceback:{self.traceback_str}"""


# if __name__ == "__main__":
#     try:
#         # simulate an error
#         a = 1/0
#         print(a)

#     except Exception as e:
#         app_exc = DocumentPortalException(e, sys)
#         logger.error(app_exc)
#         raise app_exc
    

import sys
import traceback
from logger.custom_logger import CustomLogger

logger = CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):
    """ Custom Exception for Document Portal """

    def __init__(self, error_message, error_details=sys):
        super().__init__(error_message)

        # Safely get traceback info
        exc_type, exc_value, exc_tb = sys.exc_info()

        if exc_tb is not None:
            self.file_name = exc_tb.tb_frame.f_code.co_filename
            self.lineno = exc_tb.tb_lineno
            self.traceback_str = ''.join(
                traceback.format_exception(exc_type, exc_value, exc_tb)
            )
        else:
            # Fallback when no traceback exists
            self.file_name = "Unknown"
            self.lineno = -1
            self.traceback_str = "No traceback available"

        self.error_message = str(error_message)

    def __str__(self):
        return (
            f"\nError in [{self.file_name}] at line [{self.lineno}]\n"
            f"Message: {self.error_message}\n"
            f"Traceback:\n{self.traceback_str}"
        )


if __name__ == "__main__":
    try:
        # simulate an error
        a = 1 / 0

    except Exception as e:
        app_exc = DocumentPortalException(e)
        logger.error(app_exc)
        raise app_exc
    




# # import sys
# # import traceback

# # class DocumentPortalException(Exception):
# #     """Custom Exception for Document Portal"""

# #     def __init__(self, message: str, original_exception: Exception):
# #         self.message = message
# #         self.original_exception = original_exception

# #         _, _, exc_tb = sys.exc_info()

# #         self.file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb else "N/A"
# #         self.lineno = exc_tb.tb_lineno if exc_tb else "N/A"

# #         self.traceback_str = "".join(
# #             traceback.format_exception(type(original_exception), original_exception, exc_tb)
# #         )

# #         super().__init__(self.message)

# #     def __str__(self):
# #         return (
# #             f"\nError in [{self.file_name}] at line [{self.lineno}]"
# #             f"\nMessage: {self.message}"
# #             f"\nCaused by: {repr(self.original_exception)}"
# #             f"\nTraceback:\n{self.traceback_str}")