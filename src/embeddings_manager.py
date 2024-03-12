from src.utils import logger, config
from langchain_community.embeddings import HuggingFaceEmbeddings


class EmbeddingsManager:
    def __init__(self):
        self.config = config.document_embeddings
        self.embeddings = None
        self.initialize_embeddings()

    def initialize_embeddings(self):
        logger.info("Initializing Hugging Face embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.model_name,
            model_kwargs=self.config.model_kwargs,
            encode_kwargs=self.config.encode_kwargs,
        )

    def get_embeddings(self):
        if not self.embeddings:
            self.initialize_embeddings()
        return self.embeddings


# Usage example
if __name__ == "__main__":
    embeddings_manager = EmbeddingsManager()
    embeddings = embeddings_manager.get_embeddings()

    query = "What is Python ?"
    query_result = embeddings.embed_query(query)

    print(len(query_result))
    print(query_result[:5])
