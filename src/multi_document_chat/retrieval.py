import sys 
import os 

from operator import itemgetter
 
from typing import List, Optional


from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import StrOutputParser 
from langchain_community.vectorstores import FAISS 
from langchain_core.runnables import RunnablePassthrough
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain 
# from langchain.chains.combine_documents import create_stuff_documents_chain 

from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException 
from logger.custom_logger  import CustomLogger 

from prompts.prompt_library import PROMPT_REGISTRY 
from model.models import PromptType





class ConversationalRAG:
    def __init__(self, session_id:str, retriever=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.llm = self._load_llm()
            self.session_id = session_id
            self.contextualize_prompt:ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXTUALIZE_QUESTION.value]
            self.qa_prompt: ChatPromptTemplate = PROMPT_REGISTRY[PromptType.CONTEXT_QA.value]

            if retriever is None:
                raise ValueError("Retriever cannot be None")
            self.retriever = retriever
            self._build_lcel_chain()
            self.log.info("ConversationalRAG initialized", session_id= self.session_id)

        except Exception as e:
            self.log.error("Failed to initialize ConversationalRAG", error=str(e))
            raise DocumentPortalException("Initialization error in ConversationalRAG", sys)

    def load_retriever_from_faiss(self, index_path:str):
        """
        Load a FAISS Vectore store from disk and convert to retriever
        """ 
        try:
            embeddings = ModelLoader().load_embeddings()
            if not os.path.isdir(index_path):
                raise FileNotFoundError (f"FAISS index directory not found: {index_path}")
            
            vectorestore = FAISS.load_local(index_path,
                                            embeddings, 
                             allow_dangerous_deserialization=True, #only if you trust the index
                             )
            self.retriever = vectorestore.as_retriever(search_type="similarity", search_kwargs={"k":5})

            self.log.info("FAISS retriever loaded successfully", 
                          index_path = index_path, session_id = self.session_id)
    
            return self.retriever
        
        except Exception as e:
            self.log.error("Failed to load retriever from FAISS", error= str(e))
            raise DocumentPortalException ("Loading error in ConversationalRAG", sys)

    def _load_llm(self):
        try:
            llm = ModelLoader().load_llm()

            if not llm:
                raise ValueError("LLM could not be loaded")
            self.log.error("LLM loaded successfully", session_id = self.session_id)
        
        except Exception as e:
            self.log.error("Failed to load llm", error= str(e))
            raise DocumentPortalException ("LLM loading error in ConversationalRAG", sys)


    def invoke(self, user_input:str, chat_history: Optional[List[BaseMessage]]=None) -> str:
        try:
            chat_history = chat_history or []
            payload = {"input": user_input, "chat_history": chat_history}
            answer = self.chain.invoke(payload) #invoking the payload

            if not answer:
                self.log.warning("No answer generated", user_input=user_input, session_id= self.session_id)
                return "no answer generated."
            
            self.log.info("Chain ivoked successfully",
                          session_id = self.session_id,
                          user_input = user_input,
                          answer_preview = answer[:150],)
            return answer

        except Exception as e:
            self.log.error("Failed to invoke ConversationaRAG", error = str(e))
            raise DocumentPortalException("Invocation error in ConversationalRAG", sys)


    @staticmethod 
    def _format_docs(docs):
        # static method doesn't have the self keyword, and cannot access the objects created by the class
        # I mean the ConversationalRAG class. It is often used as a utility function.
        # in format_docs whatever content we return we join it as page content
        return "n\n".join(d.page_content for d in docs)

    def _build_lcel_chain(self):
        try:
            # rewrite questions using chathistory
            question_rewriter = (
                {"input": itemgetter("input"), "chat_history": itemgetter("chat_history")}
                | self.qa_prompt
                | self.llm
                | StrOutputParser
            )
             # retrieve docs for rewritten questions
            retrieve_docs = question_rewriter | self.retriever | self._format_docs #this is called a sequential chain

            # feed context + original input + + chat hsitory into answer prompt
            self.chain = (
                {"context": retrieve_docs,
                    "input": itemgetter("input"), #itemgetter will iterate over every input and generate output
                    "chat_history": itemgetter("chat_history"),
                }
                | self.qa_prompt
                | self.llm
                | StrOutputParser()
            )
            self.log.info("LCEL chain buil successfully", session_id = self.session_id)
                 
        except Exception as e:
            self.log.error("Failed to build lcel chain", error = str(e))
            raise DocumentPortalException("LCEL chain failed", sys)
