import os
import sys

# load environment variables
from dotenv import load_dotenv

# load configuration
from utils.config_loader import load_config

# load Embedding Model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

# load logger and exception modules
from logger.custom_logger import  CustomLogger
from exception.custom_exception import DocumentPortalException

# create a variable of the logger
log = CustomLogger().get_logger(__name__)


# Create a Model Loader Class
class ModelLoader:
    """
    A utility class to load embedding models and LLM models
    """
    def __init__(self):

        load_dotenv()

        self.config = load_config()
        self._validate_env()
        log.info("Configuration loaded successfully", config_keys=list(self.config.keys()))
       

    def _validate_env(self):
        """
        Validate the necessary environment variables
        Ensure API keys exist
        """
        required_vars = ["GROQ_API_KEY", "OPENAI_API_KEY"]
        self.api_keys = {key:os.getenv(key)  for key in required_vars}
        missing = [k for k, v in self.api_keys.items()    if not v] # k, v represent key, value, if v is not there, write the key name

        # if something is missing in the list, we'll log the error message
        if missing:
            log.error("missing environment variables", missing_vars = missing)  # log the error message
            raise DocumentPortalException("Missing environment variables", sys) # sys for traceback
        
        # else if everything is fine, if the keys are all there, we'll log the info too
        log.info("Environment variables validated", available_keys = [k for k in self.api_keys if self.api_keys[k]])


    def load_embeddings(self):
        """
        Load the embedding model
        """
        try:
            log.info("loading the embedding model...")
            model_name = self.config["embedding_model"]["model_name"]
            return OpenAIEmbeddings(model = model_name)
        
        except Exception as e:
            log.error("Error loading embedding model", error = str(e))
            raise DocumentPortalException("Failed to load embedding_model", sys)

    def load_llm(self):
        """
        Load and return the LLM model
        """
        """load and return the LLM dynamically based on provider in config"""

        llm_block = self.config["llm"] # llm_block from config.yaml

        provider_key = os.getenv("LLM_PROVIDER", "openai") #default llm provider openai, check and get the llm provider  environment variable

        if provider_key not in llm_block:
            log.error("LLM provider not found in config", provider_key = provider_key)
            raise ValueError(f"Provider '{provider_key}'  not found in config")
        
        # collect every llm (provider_key) detail from the config.yaml
        llm_config = llm_block[provider_key]
        provider = llm_config.get("provider")
        model_name = llm_config.get("model_name")
        temperature = llm_config.get("temperature", 0.2)
        max_tokens = llm_config.get("max_tokens")

        log.info("Loading llm", provider=provider, model=model_name, temperature=temperature, max_tokens=max_tokens)


        if provider == "openai":
            llm = ChatOpenAI(
                model=model_name,
                api_key=self.api_keys["OPENAI_API_KEY"],
                temperature=temperature,
                max_tokens=max_tokens)
            return llm
        
        elif provider == "groq":
            llm = ChatGroq(
                model=model_name,
                api_key=self.api_keys["GROQ_API_KEY"], #type: ignore
                temperature=temperature,)
            return llm
        
        else:
            log.error("Unsupported LLM provider", provider = provider)
            raise ValueError(f"Unsupported LLM provider: {provider}")


if __name__ == "__main__": 
    loader = ModelLoader()

    #Test the embedding model loading
    embeddings = loader.load_embeddings()
    print(f"Embedding Model Loaded: {embeddings}")

    #Test LLM loading based on YAML config
    llm = loader.load_llm()
    print(f"LLM Loaded: {llm}")

    #Test the Model Loader
    result = llm.invoke("Hello, how are you?")
    print(f"LLM Result: {result.content}")


