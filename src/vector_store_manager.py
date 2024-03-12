from src.utils import logger, config
from langchain_community.vectorstores import Chroma
from src.document_extractor import DocumentExtractor
from src.document_loader import DocumentLoader
from src.embeddings_manager import EmbeddingsManager
from src import dirs


class VectorStoreManager:
    def __init__(self):
        self.vector_store = None

    def create_vector_store(self, documents, embeddings, vector_store_dir):
        logger.info("Creating a vector store for the documents...")
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            # persist_directory=vector_store_dir,
        )

    def get_vector_store(self):
        if not self.vector_store:
            raise ValueError("Vector store has not been created yet.")
        return self.vector_store


# Usage example
if __name__ == "__main__":
    # Extract documents
    document_extractor = DocumentExtractor()
    query = "What is Python ?"
    document_extractor.crawl_and_extract(
        documents_dir=str(dirs.DOCUMENTS_DIR),
        url="https://en.wikipedia.org/wiki/Python_(programming_language)",
        query=query,
    )

    # Load documents
    document_loader = DocumentLoader()
    documents_dir = str(dirs.DOCUMENTS_DIR)
    documents = document_loader.load_and_split_documents(documents_dir)

    # Initialize embeddings
    embeddings_manager = EmbeddingsManager()
    embeddings = embeddings_manager.get_embeddings()

    # Create vector store
    vector_store_manager = VectorStoreManager()
    vector_store_manager.create_vector_store(documents, embeddings, str(dirs.VECTOR_STORE_DIR))
    vector_store = vector_store_manager.get_vector_store()

    # Basic example
    results = vector_store.similarity_search(query, k=10)

    print(f"Top {len(results)} documents similar to the query '{query}':\n")

    for i, result in enumerate(results, start=1):
        document_content = result.page_content
        document_source = result.metadata['source']

        print(f"Document {i}:")
        print(f"Source: {document_source}")
        print(f"Content: {document_content}\n")
