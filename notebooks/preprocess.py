import re
import string
import unicodedata
import inflect

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def remove_equations(text):
    # Remove digits and mathematical equations
    text = re.sub(r'\$.*?\$', '', text)
    return text

def remove_punctuation(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def to_lowercase(text):
    # Convert to lowercase
    text = text.lower()
    return text

def remove_accents(text):
    # Remove accents from Latin letters
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8', 'ignore')
    return text

def tokenize_and_remove_stopwords(text):
    # Tokenize the text
    words = nltk.word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Join the processed words back into a sentence
    processed_text = ' '.join(words)
    return processed_text

def lemmatize_text(text):
    # Lemmatize the text
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    
    # Join the lemmatized words back into a sentence
    processed_text = ' '.join(lemmatized_words)
    return processed_text

def number_to_text(text):
    # Convert digits to text representation
    p = inflect.engine()
    words = []
    for word in text.split():
        if word.isdigit():
            words.append(p.number_to_words(word))
        else:
            words.append(word)
    processed_text = ' '.join(words)
    return processed_text

def stem_text(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Initialize the Porter stemmer
    stemmer = PorterStemmer()
    
    # Stem each word in the text
    stemmed_words = [stemmer.stem(word) for word in words]
    
    # Join the stemmed words back into a sentence
    processed_text = ' '.join(stemmed_words)
    
    return processed_text

def remove_website_links(text):
    # Regular expression to match website links
    processed_text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)
    
    return processed_text
