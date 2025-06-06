
![goty](https://github.com/user-attachments/assets/71d50555-0bc8-4c31-9a2e-35562319d4aa)

# Sentiment Analysis of Game of the Year Reviews on Steam

This repository contains the source code, analysis, and resources for the undergraduate thesis titled "Sentiment Analysis of Game of the Year (GOTY) Reviews on the Steam Platform using BERT". The project aims to analyze user sentiment for GOTY-winning games to explore the potential divergence between critical acclaim and player perception.

## Key Analyses

This research performs several key analyses on a dataset of over 650,000 user reviews:

* **Sentiment Classification:** Classifies each review into a binary sentiment (Positive or Negative) using a pre-trained BERT model.
* **Sentiment Trend Analysis:** Visualizes the volume of positive and negative reviews over time to identify how player perception evolves post-launch.
* **Dominant Aspect Identification:** Identifies and quantifies the most frequently discussed aspects of the games (e.g., Story, Gameplay, Performance, Difficulty) within positive and negative reviews.

## Methodology & Tech Stack

The analysis pipeline was developed using Python in a Jupyter Notebook environment.

* **Data Source:** User reviews for GOTY winners (2014-2024) were collected from the Steam platform via web scraping.
* **Core Model:** Sentiment analysis was performed using the `nlptown/bert-base-multilingual-uncased-sentiment` model from the Hugging Face Transformers library.
* **Long Text Handling:** A content selection strategy was implemented to process reviews exceeding BERT's 512-token limit by creating a representative summary from the start, middle, and end sections of the original text.
* **Tech Stack:**
    * **Programming Language:** Python 3
    * **Core Libraries:** Pandas, NumPy, scikit-learn, PyTorch
    * **NLP:** Hugging Face Transformers
    * **Web Scraping:** BeautifulSoup, Requests
    * **Visualization:** Matplotlib, Seaborn

## Key Findings

* While the overall sentiment towards GOTY-winning games is predominantly positive (with a model accuracy of ~89%), there is significant variance in reception between different
