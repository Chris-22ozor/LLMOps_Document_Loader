import os
import sys
from utils.model_loader import ModelLoader

### egg-info file contains metadata from the setup.py file

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException

from model.models import *

from langchain_core.output_parsers import JsonOutputParser 
# from langchain.output_parsers import OutputFixingParser 

from prompts.prompt_library import *


class DocumentAnalyzer:
    """
    Analyzes documents using a pre-trained model
    Automatically logs all actions and supports session-based organization
    """

    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            # prepare parsers

            self.parser = JsonOutputParser(pydantic_object=Metadata, llm=self.llm)
            # self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

            self.prompt = prompt

            self.log.info("DocumentAnalyzer initialized successfully")

        except Exception as e:
            # self.log.error("Error Initializing DocumentAnalyzer", exc_info=True)
            self.log.error(f"Error Initializing DocumentAnalyzer: {e}")
            raise DocumentPortalException ("Error in Document Analyzer initialization", sys)
        
    def analyze_document(self, document_text:str) -> dict:
        """
        Analyze a document's text and extract structured metadata & summary
        Analysis of the document is also called meta data analysis
        """
        try:
            chain = self.prompt | self.llm |self.parser

            self.log.info("Meta-data analysis chain initialized")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })
            self.log.info("Metadata extraction successful", keys=list(response.keys()))

            return response
        
        except Exception as e:
            # self.log.error("Metadata analysis failed", exc_info=True)
            self.log.error("Metadata analysis failed", error=str(e))
            # self.log.error("Metadata analysis failed", error= {e})
            
            raise DocumentPortalException ("Metadata extraction failed", sys)

        
        # try:
        #     model = self.model_loader.load_model()
        #     analysis_result = model.analyze(document_path)
        #     return self.fixing_parser.parse(analysis_result)
        # except Exception as e:
        #     raise DocumentPortalException("Error analyzing document", e) from e
       









