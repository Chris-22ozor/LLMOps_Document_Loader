import sys 
from pathlib import Path 
import fitz #PyMUPDF

from logger import custom_logger 
from exception.custom_exception import DocumentPortalException 



class DocumentComparator:
    """
    Save, read , delete & combine PDFs for comparison with session-based versioning  
    its more about file loading
    """

    def __init__(self):
        pass

    def delete_existing_files(self):
        """
        Delete existing files at the specific path

        """
        pass 

    def save_uploaded_files(self):
        """
        Save uploaded files to a specific directory
        """
        pass


    def read_pdf(self):
        """Read a PDF file and extract texts from each page
        """
        pass
