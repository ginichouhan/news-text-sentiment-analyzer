# 🧠 NLP Text Analysis on News Articles .

This project was part of a Data Science . It involves web scraping of article content from provided URLs and performing **Natural Language Processing (NLP)** to extract meaningful metrics.

---

## 📌 Objective

- Extract article content (title + text) from the list of URLs provided in `Input.xlsx`.
- Perform text analysis on each article and compute metrics like:
  - Sentiment scores (Positive, Negative, Polarity, Subjectivity)
  - Readability (FOG Index, Complex Words %, Avg. Sentence Length)
  - Word statistics (Word Count, Personal Pronouns, Avg. Word Length)

---

## 🛠️ Tech Stack

- **Python**
- **BeautifulSoup / Selenium / Requests**
- **NLTK / TextBlob / Regex**
- **Pandas, NumPy**
- **OpenPyXL / CSV**
- **Jupyter Notebook (optional)**

---

## 📂 Folder Structure

```
news-text-sentiment-analyzer/
│
├── Input.xlsx
├── Output.csv
├── text_files/           # Contains one .txt file per article (named by URL_ID)
├── analysis.py           # Python script for scraping + analysis
├── instructions.md       # Step-by-step guide to run the project
├── requirements.txt      # Python libraries used
└── README.md             # This file
```

---

## 📊 Output Metrics

| Metric                    | Description |
|---------------------------|-------------|
| POSITIVE SCORE            | Total positive words |
| NEGATIVE SCORE            | Total negative words |
| POLARITY SCORE            | (Positive - Negative) / (Positive + Negative + ε) |
| SUBJECTIVITY SCORE        | Subjective words ratio |
| AVG SENTENCE LENGTH       | Total words / Total sentences |
| PERCENTAGE OF COMPLEX WORDS | Complex words (3+ syllables) ratio |
| FOG INDEX                 | Readability score |
| PERSONAL PRONOUNS         | Count of personal pronouns |
| AVG WORD LENGTH           | Total characters / Total words |

---

## 🚀 How to Run

1. Clone this repository  
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Place `Input.xlsx` in root folder  
4. Run:
   ```
   python analysis.py
   ```
5. Output:
   - All articles saved in `/text_files/`
   - Analysis results saved in `Output.csv`

---

## 📎 Notes

- Article scraping excludes site headers/footers
- All outputs follow the format in `Output Data Structure.xlsx`
- Libraries used: BeautifulSoup, NLTK, TextBlob, Pandas

---

## 👩‍💻 Project by

**Ragini Chouhan**  
[LinkedIn](https://www.linkedin.com/in/ragini-chouhan-a64a711a0/)

---

