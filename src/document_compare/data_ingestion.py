import sys 
from pathlib import Path 
import fitz #PyMUPDF

from logger.custom_logger import CustomLogger 
from exception.custom_exception import DocumentPortalException 



class DocumentIngestion:
    """
    Save, read , delete & combine PDFs for comparison with session-based versioning  
    its more about file loading
    """

    def __init__(self, base_dir):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir) # this shows the path where we will get the data 
        self.base_dir.mkdir(parents=True, exist_ok =True) # this will create the directory if it doesn't exist



    def delete_existing_files(self):
        """
        Delete existing files at the specific path

        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error deleting existing files: {e}")
            raise DocumentPortalException ("Error occurred while deleting existing files", sys) 

    def save_uploaded_files(self):
        """
        Save uploaded files to a specific directory
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException ("Error occurred while saving uploaded files", sys)


    def read_pdf(self, pdf_path:Path) -> str:
        """Read a PDF file and extract texts from each page
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted():
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                
            all_text = []  # extracting all text in a list
            for page_num in range(doc.page_count):
                doc.load_page(page_num)
                text = page.get_text() # type: ignore
                if text.strip():
                    all_text.append(f"\n ----- Page {page_num + 1 }----- \n{text}")

            self.log.info("PDF read successfully", file= str(pdf_path), pages =len(all_text))





        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException ("Error reading PDF", sys)
