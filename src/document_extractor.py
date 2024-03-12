from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from src.utils import logger, config
from src import dirs
from src.keyword_extractor import KeywordExtractor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from scipy.sparse import vstack


class DocumentExtractor:
    def __init__(self):
        self.config = config.document_extraction
        self.keyword_extractor = KeywordExtractor()
        self.tfidf_vectorizer = TfidfVectorizer()
        self.paragraphs_vectorized = None

    @staticmethod
    def is_internal_url(found_url, base_url):
        """Check if the URL is internal to the base URL."""
        return urlparse(found_url).netloc == urlparse(base_url).netloc

    def fetch_internal_links(self, url, visited):
        """Fetch all internal links from a given webpage."""
        internal_links = set()
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                if self.is_internal_url(full_url, url) and full_url not in visited:
                    internal_links.add(full_url)
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return internal_links

    def is_redundant(self, new_paragraph):
        """Check if the new paragraph is too similar to any of the already added paragraphs."""
        if self.paragraphs_vectorized is None:
            return False

        new_vec = self.tfidf_vectorizer.transform([new_paragraph])
        similarity_scores = cosine_similarity(new_vec, self.paragraphs_vectorized)
        return np.max(similarity_scores) > self.config.redundancy_similarity_threshold

    def add_paragraph_vectorized(self, paragraph):
        """Add the new paragraph to the vectorized matrix for future similarity checks."""
        if self.paragraphs_vectorized is None:
            self.paragraphs_vectorized = self.tfidf_vectorizer.fit_transform([paragraph])
        else:
            new_vec = self.tfidf_vectorizer.transform([paragraph])
            self.paragraphs_vectorized = vstack([self.paragraphs_vectorized, new_vec])

    def extract_relevant_text(self, soup, keywords, max_docs, use_similarity=False):
        """Extract relevant text from a BeautifulSoup object based on keywords."""
        keyword_docs = None
        if use_similarity:
            keyword_docs = [self.keyword_extractor.nlp(keyword) for keyword in keywords]

        relevant_texts = []
        for p in soup.find_all('p'):
            paragraph_text = p.get_text(strip=True)

            # Skip short paragraphs
            if len(paragraph_text) < self.config.min_length_threshold:
                continue

            # Skip paragraphs with too high keyword density
            keyword_occurrences = sum(keyword.lower() in paragraph_text.lower() for keyword in keywords)
            keyword_density = keyword_occurrences / (len(paragraph_text.split()) + 1)
            if keyword_density > self.config.keyword_density_threshold:
                continue

            # Skip redundant paragraphs
            if self.is_redundant(paragraph_text):
                continue

            if any(keyword.lower() in paragraph_text.lower() for keyword in keywords):
                relevant_texts.append(paragraph_text)
                self.add_paragraph_vectorized(paragraph_text)
                if len(relevant_texts) >= max_docs:
                    break

            elif use_similarity:
                paragraph_doc = self.keyword_extractor.nlp(paragraph_text)
                if paragraph_doc.has_vector:
                    if any(paragraph_doc.similarity(keyword_doc) > self.config.keyword_similarity_threshold for
                           keyword_doc in keyword_docs):
                        relevant_texts.append(paragraph_text)
                        self.add_paragraph_vectorized(paragraph_text)
                        if len(relevant_texts) >= max_docs:
                            break

        return relevant_texts

    def crawl_and_extract(self, documents_dir, url, query, user_keywords=None):
        """Crawl from the given URL and extract relevant text based on keywords."""
        if user_keywords is None:
            user_keywords = []

        visited = set()
        pages_to_visit = {url}
        all_relevant_texts = []

        # Use KeywordExtractor to augment user-defined keywords
        extracted_keywords = self.keyword_extractor.extract_keywords(query)
        keywords = list(set(user_keywords + extracted_keywords.combined))

        while (pages_to_visit and len(visited) < self.config.max_pages and len(
                all_relevant_texts) < self.config.max_docs):
            current_url = pages_to_visit.pop()
            if current_url in visited:
                continue
            if self.config.verbose:
                logger.info(f"Visiting: {current_url}")
            visited.add(current_url)

            try:
                response = requests.get(current_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                relevant_texts = self.extract_relevant_text(soup, keywords,
                                                            self.config.max_docs - len(all_relevant_texts))
                all_relevant_texts.extend(relevant_texts)

                if len(all_relevant_texts) >= self.config.max_docs:
                    break

                # Fetch internal links and add them to the pages to visit
                internal_links = self.fetch_internal_links(current_url, visited)
                pages_to_visit.update(internal_links)

            except requests.RequestException as e:
                if self.config.verbose:
                    logger.error(f"Error fetching content from {current_url}: {e}")

        if not all_relevant_texts:
            logger.info("No relevant documents found based on the provided keywords.")
            return

        # file_name = urlparse(url).netloc.replace("www.", "") + "_extracted.txt"
        file_name = "extracted.txt"
        file_path = Path(documents_dir) / file_name

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n\n".join(all_relevant_texts))

        logger.info(f"Document containing {len(all_relevant_texts)} relevant sections saved to {file_path}")


# Usage example
if __name__ == "__main__":
    document_extractor = DocumentExtractor()
    query = "What is Python ?"
    document_extractor.crawl_and_extract(
        documents_dir=str(dirs.DOCUMENTS_DIR),
        url="https://en.wikipedia.org/wiki/Python_(programming_language)",
        query=query,
    )
