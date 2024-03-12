from src.utils import config
from box import Box
import spacy
import pytextrank


class KeywordExtractor:
    def __init__(self):
        self.config = config.keyword_extraction

        # Load SpaCy model
        self.nlp = spacy.load(self.config.model_name)

        # Add PyTextRank to the spaCy pipeline
        self.nlp.add_pipe("textrank")

    def extract_keywords_fallback(self, text):
        """Fallback method to use query words as keywords."""
        doc = self.nlp(text)
        print(doc)
        return [token.text for token in doc if not token.is_stop and not token.is_punct]

    def extract_keywords(self, text):
        """Process text and extract keywords using NER, POS tagging, and TextRank."""
        doc = self.nlp(text)

        # NER Keywords
        keywords_ner = [ent.text for ent in doc.ents]

        # POS Keywords
        keywords_pos = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB']]

        # TextRank Keywords
        keywords_textrank = [phrase.text for phrase in doc._.phrases[:10] if phrase.rank > 0.]

        # keywords_textrank = []
        # for phrase in doc._.phrases[:10]:
        #     if phrase.rank > 0.1:
        #         keywords_textrank.extend(phrase.text.split())

        # Combine and deduplicate keywords, prioritizing TextRank keywords
        combined_keywords = list(dict.fromkeys(keywords_textrank + keywords_pos + keywords_ner))

        if not combined_keywords:
            combined_keywords = self.extract_keywords_fallback(text)

        return Box({
            'ner': list(set(keywords_ner)),
            'pos': list(set(keywords_pos)),
            'textrank': list(set(keywords_textrank)),
            'combined': combined_keywords
        })


# Usage example
if __name__ == "__main__":
    query = "I'm interested in learning about machine learning applications in finance."

    keyword_extractor = KeywordExtractor()
    extracted_keywords = keyword_extractor.extract_keywords(query)

    print(f"Query: {query}")
    print(f"NER Keywords: {extracted_keywords.ner}")
    print(f"POS Keywords: {extracted_keywords.pos}")
    print(f"TextRank Keywords: {extracted_keywords.textrank}")
    print(f"Combined Keywords: {extracted_keywords.combined}")

