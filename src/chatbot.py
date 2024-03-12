from pathlib import Path
from src.utils import logger, config
from src.document_loader import DocumentLoader
from src.embeddings_manager import EmbeddingsManager
from src.vector_store_manager import VectorStoreManager
from huggingface_hub import hf_hub_download
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain.prompts import (ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder,
#                                SystemMessagePromptTemplate, PromptTemplate)
from src import dirs


class ChatBot:
    def __init__(self):
        self.config = config.chatbot
        self.document_loader = DocumentLoader()
        self.embeddings_manager = EmbeddingsManager()
        self.vector_store_manager = VectorStoreManager()
        self.llm = None
        self.llm_params = self.config.llm_params
        self.retrieval_chain = None

    def setup_language_model(self):
        logger.info("Initializing the language model...")
        llm_name = self.config.llm_name
        llm_path = dirs.MODELS_DIR / llm_name
        if not llm_path.exists():
            hf_hub_download(
                repo_id=self.config.hf_repo_id,
                filename=llm_name,
                cache_dir=str(dirs.MODELS_DIR),
            )
        self.llm = LlamaCpp(
            model_path=str(llm_path),
            temperature=self.llm_params.temperature,
            max_tokens=self.llm_params.max_tokens,
            top_p=self.llm_params.top_p,
            n_gpu_layers=self.llm_params.n_gpu_layers,
            n_batch=self.llm_params.n_batch,
            n_ctx=self.llm_params.n_ctx,
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
            verbose=self.llm_params.verbose,
        )

    def setup_retrieval_chain(self):
        logger.info("Configuring the Conversational Retrieval chain...")

        retriever = self.vector_store_manager.get_vector_store().as_retriever(
            search_kwargs=self.config.retriever_params.search_kwargs
        )

        memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            memory_key=self.config.memory_params.memory_key,
            return_messages=self.config.memory_params.return_messages,
            max_token_limit=self.config.memory_params.max_token_limit,
            output_key=self.config.memory_params.output_key,
        )

        self.retrieval_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            chain_type=self.config.chain_type,
            memory=memory,
            return_source_documents=self.config.return_source_documents,
            return_generated_question=self.config.return_generated_question,
            verbose=self.config.verbose,
            get_chat_history=lambda h: h,
        )

    def setup_chatbot(self, documents_dir=str(dirs.DOCUMENTS_DIR)):
        # Load and process documents
        documents = self.document_loader.load_and_split_documents(documents_dir)
        # Initialize embeddings
        embeddings = self.embeddings_manager.get_embeddings()
        # Initialize vector store
        self.vector_store_manager.create_vector_store(documents, embeddings, str(dirs.VECTOR_STORE_DIR))
        # Setup language model
        self.setup_language_model()
        # Setup retrieval chain
        self.setup_retrieval_chain()

    def ask_question(self, question):
        logger.info("Invoking the chain for question-answering...")
        response = self.retrieval_chain.invoke(
            {
                "question": question,
                # "chat_history": chat_history,
            },
        )

        # print(f"- response.keys() = {response.keys()}")
        # print(f"- response['chat_history'] = {response['chat_history']}")

        return response["answer"]


# Usage example
if __name__ == "__main__":
    chatbot = ChatBot()
    chatbot.setup_chatbot(dirs.DOCUMENTS_DIR)
    question = "What is Python ?"
    response = chatbot.ask_question(question)
    # response = chatbot.llm.invoke(question)
    print(f"\nQuestion: {question}\nResponse:{response}")

    # question = "What did I ask you previously ?"
    # response = chatbot.ask_question(question)
    # # response = chatbot.llm.invoke(question)
    # print(f"\nQuestion: {question}\nResponse:{response}")

