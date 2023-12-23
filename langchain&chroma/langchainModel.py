import os
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from utils import chroma_client, INDEX_NAME

class LangchainModel:
    
    @classmethod
    def initialize_model(cls):
        # Import statements (if not already at the top of your file)
        template = """
        Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question:
        ------
        <ctx>{context}</ctx>
        ------
        <hs>{history}</hs>
        ------
        {question}
        Answer:
        """
        prompt_template = PromptTemplate(
            input_variables=["history", "context", "question"],
            template=template,
        )
        conversation_memory = ConversationBufferMemory(
            memory_key="history",
            input_key="question"
        )
        api_key = os.environ.get("OPENAI_API_KEY", "default_api_key") # Handle missing API key
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vstore = Chroma(client=chroma_client,
                        collection_name=INDEX_NAME,
                        embedding_function=embeddings)

        retriever = vstore.as_retriever(search_kwargs={"k": 4})

        cls.model = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            chain_type='stuff',
            retriever=retriever,
            chain_type_kwargs={
                "prompt": prompt_template,
                "memory": conversation_memory
            })

    @staticmethod
    def query(question, memory):
        if not LangchainModel.model:
            raise ValueError("Model not initialized")
        print('\nMemory session',memory,'\nMemory variables', LangchainModel.model.memory)
        return LangchainModel.model.run(question)
