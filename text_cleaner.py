import spacy
import contractions
import re

class TextCleaner:
    def __init__(self, model="en_core_web_sm", custom_stopwords=None, keep_words=None):
        self.nlp = spacy.load(model)

        # Add POS tags to keep
        self.accepted_pos = {"NOUN", "VERB", "AUX", "ADJ", "INTJ", "PROPN"}

        # Allow user-defined stopword removal
        self.custom_stopwords = set(custom_stopwords) if custom_stopwords else {"let", "shall"}

        # Words to force keep even if spaCy considers them stopwords
        self.keep_words = set(keep_words) if keep_words else {"go", "do", "be"}

        # Override spaCy stopwords if needed
        for word in self.keep_words:
            self.nlp.vocab[word].is_stop = False
            if word in self.nlp.Defaults.stop_words:
                self.nlp.Defaults.stop_words.remove(word)

    def is_emoji(self, text):
        return bool(re.fullmatch(r"[\U00010000-\U0010ffff]", text))

    def clean(self, paragraph):
        paragraph = contractions.fix(paragraph)
        doc = self.nlp(paragraph)
        cleaned_sentences = []

        for sent in doc.sents:
            words = []
            for token in sent:
                if token.is_stop or token.is_punct or token.like_url or token.like_num:
                    continue
                if token.text.lower() in self.custom_stopwords:
                    continue
                if token.text.startswith('#') or token.text.startswith('@'):
                    continue
                if not token.text.isalpha() and not self.is_emoji(token.text):
                    continue
                if not (self.is_emoji(token.text) or token.pos_ in self.accepted_pos):
                    continue

                words.append(token.lemma_.lower())

            if words:
                cleaned_sentences.append(' '.join(words))

        return cleaned_sentences
