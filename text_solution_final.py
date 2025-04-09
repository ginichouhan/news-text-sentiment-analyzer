# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 17:59:14 2025

@author: ragin
"""

# ---------------------------------------------
# Text Extraction and Sentiment Analysis Script
# ---------------------------------------------
# Description:
# - Extracts content from URLs
# - Preprocesses the text
# - Performs sentiment and readability analysis
# - Saves results in Excel and individual .txt files

# ---------------------------------------------
# Required Libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import string
import re

#Paths
MASTER_DICTIONARY_PATH = r"C:\Users\ragin\OneDrive\Desktop\Blackcoffer\MasterDictionary"
STOPWORDS_PATH = r"C:\Users\ragin\OneDrive\Desktop\Blackcoffer\StopWords"
OUTPUT_FILE_PATH = r"C:\Users\ragin\OneDrive\Desktop\Blackcoffer\output Data Structure.xlsx"  # <-- Updated output path
ARTICLES_FOLDER = r"C:\Users\ragin\OneDrive\Desktop\Blackcoffer\Articles"

#Create the Articles folder if it doesn't exist
os.makedirs(ARTICLES_FOLDER, exist_ok=True)

#Load positive and negative words
def load_dictionary():
    pos_file = os.path.join(MASTER_DICTIONARY_PATH, "positive-words.txt")
    neg_file = os.path.join(MASTER_DICTIONARY_PATH, "negative-words.txt")

    with open(pos_file, "r") as f:
        positive_words = set(f.read().splitlines())

    with open(neg_file, "r") as f:
        negative_words = set(f.read().splitlines())

    return positive_words, negative_words

#Load stopwords
def load_stopwords():
    stopwords = set()
    for file in os.listdir(STOPWORDS_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(STOPWORDS_PATH, file), "r") as f:
                stopwords.update(f.read().splitlines())
    return stopwords

#Clean text function
def clean_text(text, stopwords):
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # Remove digits
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return " ".join(words)

#Extract content from URL
def extract_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        
        #Extract paragraphs
        paragraphs = soup.find_all("p")
        article_text = " ".join([para.get_text() for para in paragraphs])
        
        return article_text
    except Exception as e:
        print(f"Error extracting {url}: {e}")
        return ""

#Sentiment analysis
def analyze_sentiment(text, pos_words, neg_words):
    words = text.split()
    positive_score = sum(1 for word in words if word in pos_words)
    negative_score = sum(1 for word in words if word in neg_words)

    total_words = len(words)
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score

#Readability metrics
def readability_metrics(text):
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]

    total_sentences = len(sentences)
    words = text.split()
    total_words = len(words)

    complex_words = sum(1 for word in words if len(word) > 6)

    avg_sentence_length = total_words / total_sentences if total_sentences > 0 else 0
    percentage_complex_words = (complex_words / total_words) * 100 if total_words > 0 else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    return avg_sentence_length, percentage_complex_words, fog_index, complex_words, total_words

#Count personal pronouns
def count_personal_pronouns(text):
    pronoun_pattern = r'\b(I|we|my|ours|us)\b'
    personal_pronouns = len(re.findall(pronoun_pattern, text, re.IGNORECASE))
    return personal_pronouns

#Average word length
def average_word_length(text):
    words = text.split()
    if len(words) == 0:
        return 0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)

#Main Execution
def main():
    #Load dictionaries and stopwords
    pos_words, neg_words = load_dictionary()
    stopwords = load_stopwords()

    #Read URLs from input Excel file
    input_file = r"C:\Users\ragin\OneDrive\Desktop\Blackcoffer\Input.xlsx"
    df = pd.read_excel(input_file)

    results = []

    for index, row in df.iterrows():
        url_id = row.get("URL_ID", f"Unknown_{index}")
        url = row.get("URL", "")

        print(f"Processing {url_id}...")

        #Extract article content
        content = extract_article_content(url)

        if content:
            #Ensure the Articles folder exists
            os.makedirs(ARTICLES_FOLDER, exist_ok=True)

            #Save the extracted content to a .txt file
            article_file_path = os.path.join(ARTICLES_FOLDER, f"{url_id}.txt")
            
            with open(article_file_path, "w", encoding="utf-8") as f:
                f.write(content)

            #Clean the text
            cleaned_text = clean_text(content, stopwords)

            #Sentiment analysis
            pos_score, neg_score, pol_score, subj_score = analyze_sentiment(cleaned_text, pos_words, neg_words)

            #Readability metrics
            avg_len, pct_complex, fog, complex_count, word_count = readability_metrics(cleaned_text)

            #Personal pronouns and word length
            personal_pronouns = count_personal_pronouns(cleaned_text)
            avg_word_length = average_word_length(cleaned_text)

            #Store results
            results.append([
                url_id, pos_score, neg_score, pol_score, subj_score,
                avg_len, pct_complex, fog, complex_count, word_count,
                personal_pronouns, avg_word_length
            ])

    #Create output DataFrame
    output_columns = [
        "URL_ID", "Positive Score", "Negative Score", "Polarity Score", "Subjectivity Score",
        "Avg Sentence Length", "% of Complex Words", "Fog Index", "Complex Word Count",
        "Word Count", "Personal Pronouns", "Avg Word Length"
    ]

    output_df = pd.DataFrame(results, columns=output_columns)

    #Save the DataFrame to Excel at specified path
    output_df.to_excel(OUTPUT_FILE_PATH, index=False)

    print(f"Analysis completed successfully! Results saved at: {OUTPUT_FILE_PATH}")

#Run the main function
if __name__ == "__main__":
    main()
