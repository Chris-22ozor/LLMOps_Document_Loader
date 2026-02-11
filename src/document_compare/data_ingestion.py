import sys 
import uuid
from pathlib import Path 
import fitz #PyMUPDF

from datetime import datetime, timezone

from logger.custom_logger import CustomLogger 
from exception.custom_exception import DocumentPortalException 



class DocumentIngestion:
    """
    Save, read , delete & combine PDFs for comparison with session-based versioning  
    its more about file loading
    """

    def __init__(self, base_dir:str = "data/document_compare", session_id=None):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir) # this shows the path where we will get the data 
        self.base_dir.mkdir(parents=True, exist_ok =True) # this will create the directory if it doesn't exist
        self.session_id = session_id or f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}" 
        # this other  part for session_id above creates the session id with the latest time
        self.session_path = self.base_dir/ self.session_id 
        self.session_path.mkdir(parents=True, exist_ok=True)

        self.log.info("DocumentComparator initialized", session_path=str(self.session_id))


    #------ Had to remove the delete function after updating the scripts with the session_id-------
    # def delete_existing_files(self):
    #     """
    #     Delete existing files at the specific path
    #     Meaning if already we have a file at the base dir, we will delete, else
    #     we will upload and save the file. The next function(action) below will take care of that
    #     """
    #     try:
    #         if self.base_dir.exists() and self.base_dir.is_dir():
    #             for file in self.base_dir.iterdir():
    #                 if file.is_file():
    #                     file.unlink()  # unlink means to delete the file
    #                     self.log.info("File deleted", path=str(file))

    #             self.log.info("Directory cleaned", directory=str(self.base_dir))

    #     except Exception as e:
    #         self.log.error(f"Error deleting existing files: {e}")
    #         raise DocumentPortalException ("Error occurred while deleting existing files", sys) 

    def save_uploaded_files(self, reference_file, actual_file):
        """
        Save uploaded files to a specific directory
        reference_file is version 2 while actual file is version 1
        """
        try:
            # self.delete_existing_files()
            # self.log.info("Existing files deleted successfully.")

            ref_path = self.base_dir/reference_file.name
            act_path = self.base_dir/actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed")
            
            # loading the reference file and actual file
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer()) #buffer means we are going to create a session

            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer()) #buffer means we are going to create a session

            self.log.info("Files saved", reference= str(ref_path), actual=str(act_path), session= self.session_id)
            return ref_path, act_path


        except Exception as e:
            self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException ("Error occurred while saving uploaded files", sys)


    def read_pdf(self, pdf_path:Path) -> str:
        """Read a PDF file and extract texts from each page
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                
                all_text = []  # extracting all text in a list
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text() # type: ignore

                    if text.strip():  # if text hast white spaces, then strip it
                       all_text.append(f"\n ----- Page {page_num + 1 }----- \n{text}") 
                self.log.info("PDF read successfully", file= str(pdf_path), pages =len(all_text))
                return "\n".join(all_text)

        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException ("Error reading PDF", sys)
        
    def combine_documents(self) -> str:
        try:
            content_dict = {}
            doc_parts = []
            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file()  and filename.suffix ==".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document: {filename}\n {content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined", count=len(doc_parts), session=self.session_id)
            return combined_text

        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combining documents", sys)
        
        
    def clean_old_sessions(self, keep_latest: int =3):

        """Optional method to delete older session folders, keeping only the latest Number as specified
        Args:
            keep_latest (int, optional): _description_. Defaults to 3.
        """

        try:
            sessions_folders = sorted([f for f in self.base_dir.iterdir() if f.is_dir()], reverse=True)

            for folder in sessions_folders[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmdir()
                self.log.info("Old session folder deleted", path=str(folder))

        except Exception as e:
            self.log.error("Error cleaning old sessions", error=str(e))
            raise DocumentPortalException ("Error cleaning old sessions", sys)