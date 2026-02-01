
import sys 
from dotenv import load_dotenv

import pandas as pd 

from logger.custom_logger import CustomLogger
from exception.custom_exception import DocumentPortalException 

from model.models import *
from prompts.prompt_library import PROMPT_REGISTRY 
from utils.model_loader import ModelLoader 

from langchain_core.output_parsers import JsonOutputParser 
# from langchain.output_parsers import OutputFixingParser 


class DocumentComparatorLLM:
    def __init__(self):
        load_dotenv()
        self.log = CustomLogger().get_logger(__name__)
        self.loader = ModelLoader()
        self.parser = JsonOutputParser(pydantic_object="SummaryResponse")
        self.prompt = PROMPT_REGISTRY["document_comparison"]
        self.chain = self.prompt | self.llm | self.parser 
        self.log.info("DocumentComparatorLLM initialized with model and parser.")

        # self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

    def compare_documents(self):
        """
        Compares two documents and returns a structured comparison
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in compare_documents: {e}")
            raise DocumentPortalException ("An error occurred while comparing documents", sys)


    def _format_response(self):
        """Format the response from the LLM into a structured format (private method in p)
        """
        try:
            pass
        except Exception as e:
            self.log.error(f"Error formatting response into DataFrame: {e}")
            raise DocumentPortalException ("An error occurred while formatting response", sys)

