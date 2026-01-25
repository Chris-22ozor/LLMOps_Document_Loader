import os
from utils.model_loader import ModelLoader

### egg-info file contains metadata from the setup.py file

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

from model.models import *

from langchain_core.output_parsers import JsonOutputParser 
from langchain_core.output_parsers import OutputFixingParser 


class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model
    Automatically logs all actions and supports session-based organization
    """

    def __init__(self):
        pass

    def analyze_document(self, document_path):
        pass
        # try:
        #     model = self.model_loader.load_model()
        #     analysis_result = model.analyze(document_path)
        #     return self.fixing_parser.parse(analysis_result)
        # except Exception as e:
        #     raise DocumentPortalException("Error analyzing document", e) from e
       









