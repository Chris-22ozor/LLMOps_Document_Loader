class ConversationalRAG:
    def __init__(self):
        pass

    def load_retriever_from_faiss(self):
        pass 

    def _load_llm(self):
        pass 

    def invoke(self):
        pass 

    @staticmethod 
    def _format_docs(docs):
        # static method doesn't have the self keyword, and cannot access the objects created by the class
        # I mean the ConversationalRAG class. It is often used as a utility function.
        pass

    def build_lcel_chain(self):
        pass