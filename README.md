# AI Support Ticket Analyzer

This project analyzes customer support tickets using AI.

### Features:
- Sentiment analysis
- Topic clustering
- Issue detection
- Dashboard visualization

### Tech stack:
- Python
- NLP
- Streamlit
- Machine Learning

## Structure

ai-support-ticket-analyzer

│

├─ data

│   └─ tickets.csv

│

├─ notebooks

│   └─ analysis.ipynb

│

├─ app.py

├─ requirements.txt

└─ README.md




## AI Support Ticket Analyzer – Pipeline Overview

1. Data Input
• Source file: data/tickets.csv  
• Loaded using pandas (pd.read_csv)  
• Only relevant columns are used for the analysis:
  - ticket_id
  - product
  - category
  - issue_description
  - resolution_notes
  - ticket_created_date

Purpose:
• Load the raw support ticket data into a dataframe so it can be processed and analyzed.


2. Text Preprocessing (Cleaning the Ticket Text)

Steps performed:
• Combine text fields:
  - issue_description
  - resolution_notes
  → into a new column called: clean_text

• Text normalization:
  - convert text to lowercase
  - remove punctuation and special characters
  - remove extra spaces

• Remove stopwords using NLTK:
  - examples: "the", "and", "is", "this", "that"
  - these words occur frequently but add little meaning

Purpose:
• Prepare the ticket text for NLP analysis.
• Reduce noise and keep only meaningful words.


3. Sentiment Analysis

Library used:
• TextBlob

Concept:
• Sentiment analysis measures the emotional tone of text.

Polarity score range:
• -1  → very negative sentiment
• 0   → neutral sentiment
• +1  → very positive sentiment

Implementation:
• A function calculates polarity for each ticket.
• The score is converted into categories:
  - positive
  - negative
  - neutral

Output:
• Results are stored in a new column:
  df["sentiment"]

Purpose:
• Understand how customers feel about their issues.
• Identify highly negative experiences.


4. Text Vectorization

Method used:
• TF-IDF (Term Frequency – Inverse Document Frequency)

Concept:
• Machine learning models cannot process raw text.
• TF-IDF converts words into numerical vectors.

How it works:
• Measures how important a word is within a document relative to the entire dataset.
• Words that appear frequently in one ticket but rarely in others receive higher weight.

Example:
• Sentence: "payment failed again"
• Converted into a vector of numerical values representing word importance.

Purpose:
• Transform text into numeric format for clustering algorithms.


5. Topic Detection (Clustering)

Algorithm used:
• HDBSCAN

Concept:
• HDBSCAN is a density-based clustering algorithm.
• It automatically groups similar tickets together without specifying the number of clusters beforehand.

Output:
• Each ticket receives a topic label:
  - topic = 0, 1, 2, ... → cluster/topic
  - topic = -1 → outlier (no clear cluster)

Example topics:
• Topic 0 → payment issues
• Topic 1 → login problems
• Topic 2 → application crashes
• Topic 3 → subscription cancellation

Purpose:
• Identify the most common customer problems automatically.


6. Insights Generation

Analysis performed:
• Count number of tickets per topic
• Analyze sentiment distribution per topic

Example insights:
• Topic: payment failures
  - 540 tickets
  - 92% negative sentiment

• Topic: login issues
  - 320 tickets
  - 80% negative sentiment

Purpose:
• Identify the most critical problems affecting customers.
• Help prioritize product improvements.


7. Visualization

Library used:
• matplotlib

Charts created:
• Tickets per Topic
  - shows which issues occur most often

• Sentiment Distribution
  - shows how customers feel overall

Purpose:
• Make patterns in the data easier to understand.
• Support quick decision making.


8. Final Output

The pipeline produces a structured dataset containing:
• ticket_id
• clean_text
• sentiment
• topic

The analysis provides:
• Top customer issues
• Sentiment per issue
• Frequency of each issue
• Visual summaries of the data


9. Pipeline Summary

tickets.csv
   ↓
Load Data (pandas)
   ↓
Text Cleaning & Stopword Removal
   ↓
Sentiment Analysis (TextBlob)
   ↓
Text Vectorization (TF-IDF)
   ↓
Topic Clustering (HDBSCAN)
   ↓
Insights & Visualization


10. Skills Demonstrated by the Project

Data Processing
• Data loading and preparation

Natural Language Processing
• Text cleaning
• Stopword removal
• Sentiment analysis
• TF-IDF vectorization

Machine Learning
• Unsupervised clustering (HDBSCAN)

Data Analysis
• Insight generation
• Data visualization
