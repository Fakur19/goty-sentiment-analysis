<div align="center">
  <img src="img/goty.png" alt="GOTY Banner" width="800"/>
</div>

# Sentiment Analysis of Game of the Year Reviews on Steam
This repository contains the source code, analysis, and resources for the undergraduate thesis titled **"Sentiment Analysis of Game of the Year (GOTY) Reviews on the Steam Platform using BERT"**. The project aims to analyze user sentiment for GOTY-winning games to explore the potential divergence between critical acclaim and player perception.

---

### Technology Stack
<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white" alt="Jupyter"/>
  <img src="https://img.shields.io/badge/Pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white" alt="PyTorch"/>
  <img src="https://img.shields.io/badge/%F0%9F%A4%97_Transformers-4051B5.svg?style=for-the-badge" alt="Hugging Face Transformers"/>
  <img src="https://img.shields.io/badge/Matplotlib-11557c.svg?style=for-the-badge&logo=matplotlib&logoColor=white" alt="Matplotlib"/>
  <img src="https://img.shields.io/badge/Seaborn-88d4dd.svg?style=for-the-badge&logo=seaborn&logoColor=white" alt="Seaborn"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit"/>
</div>

---

### 📊 Interactive Dashboard
An interactive dashboard has been developed using **Streamlit** to explore the dataset and model predictions dynamically. You can filter by game, view sentiment distributions, and analyze key aspects in real-time.

**[➡️ Click here to access the Streamlit Web App](https://goty-sentiment-analysis.streamlit.app/)**


![Streamlit App Screenshot](img/ss1.png)

---

## 📈 Visualizations & Key Findings
The analysis of over 650,000 user reviews reveals key trends in player sentiment and the aspects they discuss most.

#### Sentiment Trend Over Time
The volume of positive (green) and negative (red) reviews evolves after a game's launch, often peaking initially and fluctuating with sales, updates, or community discourse.

<div align="center">
  <img src="img/tw3.png" alt="Sentiment Trend Facet Grid" width="800"/>
</div>

#### Dominant Aspect Proportions
The focus of discussion varies significantly between games. While some are praised for their story, others are discussed more for their difficulty and combat, showcasing unique player priorities for each title.

<div align="center">
  <img src="img/dominant-aspect.png" alt="Aspect Proportions Chart" width="800"/>
</div>

### Summary of Findings
- While the overall sentiment towards GOTY-winning games is predominantly positive (with a model accuracy of **~89%**), there is significant variance in reception between different titles.
- **Story** and **Gameplay** are the most frequently discussed aspects across all reviews.
- **Positive reviews** often highlight **Story**, **Gameplay**, and **Graphics**.
- **Negative reviews** frequently focus on **Performance** issues (bugs, crashes, optimization) and **Difficulty**.

---

## 🔬 Methodology Overview

* **Data Source:** User reviews for GOTY winners (2014-2024) were collected from the Steam platform via **web scraping**.
* **Core Model:** Sentiment analysis was performed using the `nlptown/bert-base-multilingual-uncased-sentiment` model from the Hugging Face Transformers library.
* **Long Text Handling:** A content selection strategy was implemented to process reviews exceeding BERT's 512-token limit by creating a representative summary from the start, middle, and end sections of the original text.
* **Key Analyses:**
    * **Sentiment Classification:** Classifies each review into a binary sentiment (Positive or Negative).
    * **Sentiment Trend Analysis:** Visualizes the volume of positive and negative reviews over time to identify how player perception evolves post-launch.
    * **Dominant Aspect Identification:** Identifies and quantifies the most frequently discussed aspects of the games (e.g., Story, Gameplay, Performance, Difficulty) within positive and negative reviews.

---

## 📂 Repository Content
- **/data**: Contains the CSV files with aspect counts for positive, negative, and all reviews.
- **/img**: Contains images and visual assets used in the README and project.
- `data_analysis.ipynb`: The main Jupyter Notebook with the full analysis pipeline.
- `analysis_with_version_control.ipynb`: Additional analysis.
- `requirements.txt`: A list of Python libraries required to run the project.

---

## 🚀 Setup and Usage

### 1. Running the Analysis Notebook
1.  Clone the repository:
    ```bash
    git clone https://github.com/Fakur19/goty-sentiment-analysis
    cd goty-sentiment-analysis
    ```
2.  Create a virtual environment and install the required packages:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
3.  Launch Jupyter Notebook and open `data_analysis.ipynb` for whole analysis and `analysis_with_version_control.ipynb` for analysis with patch/update/dlc for each game.
    ```bash
    jupyter notebook
    ```
---