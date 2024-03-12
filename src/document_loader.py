from pathlib import Path
from src.utils import logger, config
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src import dirs


class DocumentLoader:
    def __init__(self):
        self.config = config.document_loader

    def load_and_split_documents(self, documents_dir):
        logger.info("Loading documents from directory...")

        # Check if the documents directory is empty
        documents_path = Path(documents_dir)
        if not any(documents_path.iterdir()):
            logger.info("The documents directory is empty. No documents to load.")
            return []

        loader = DirectoryLoader(documents_dir)
        documents = loader.load()

        logger.info("Splitting loaded documents into manageable chunks...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap
        )
        split_documents = text_splitter.split_documents(documents)

        return split_documents


# Usage example
if __name__ == "__main__":
    document_loader = DocumentLoader()
    documents_dir = str(dirs.DOCUMENTS_DIR)
    documents = document_loader.load_and_split_documents(documents_dir)

    print(f"Number of documents loaded: {len(documents)}")

    # for doc in documents:
    #     print(f"Document Source: {doc.metadata['source']}, Length: {len(doc.page_content)} characters")
