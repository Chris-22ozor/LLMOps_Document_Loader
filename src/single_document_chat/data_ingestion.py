import uuid 
from pathlib import Path 
import sys

from datetime import datetime, timezone

from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.vectorstores import FAISS  

from logger.custom_logger import CustomLogger 
from exception.custom_exception import DocumentPortalException 

from utils.model_loader import ModelLoader 


class SingleDocIngestor:
    def __init__(self, data_dir:str = "data/single_document_chat", faiss_dir:str ="faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__) #initialize the logger

            self.data_dir = Path(data_dir) #initialize the data_dir path
            self.data_dir.mkdir(parents=True, exist_ok=True)

            self.faiss_dir = Path(faiss_dir) #initialize the faiss_dir path
            self.faiss_dir.mkdir(parents=True, exist_ok=True) 

            self.model_loader =ModelLoader() #initialize the model loader
            self.log.info("SingleDocIngestor initialized", temp_path= str(self.data_dir), faiss_dir= str(self.faiss_dir))

        except Exception as e:
            self.log.error("Failed to initialize SingleDocIngestor", error= str(e))
            raise DocumentPortalException("Error during file ingestion", sys)
        
    def ingest_files(self, uploaded_files):
        try:
            documents = []

            for uploaded_file in uploaded_files:
                unique_filename = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
                temp_path = self.data_dir/unique_filename

                with open(temp_path, "wb") as f_out:
                    f_out.write(uploaded_file.read())
                self.log.info("PDF saved for ingestion", filename=uploaded_file.name)

                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)
                return self._create_retriever(documents)

        except Exception as e:
            self.log.error("Document ingestion failed", error=str(e))
            raise DocumentPortalException("Error during file ingestion", sys) 
        
    def _create_retriever(self, documents):
        try:
            pass

        except Exception as e:
            self.log.error("Retriever creation failed", error=str(e))
            raise DocumentPortalException("Error creating FAISS retriever", sys)


