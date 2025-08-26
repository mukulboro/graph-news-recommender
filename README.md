# Nepali News Aggregator Powered by ML and Graph Theory

This repository contains the backend code for **Hulaki**, a news aggregator and recommendation system. This project was developed as a 6th-semester project and is the basis for the research paper, "A Novel Approach To News Aggregation and Recommendation Using Clustering Algorithms and Graph Theory."

## 📌 About the Project

In an era of information overload, it's challenging to keep up with the news without encountering duplicate stories from different sources. This project aims to solve this problem by:

1.  **Aggregating news** from various Nepali news portals.
2.  **Clustering similar news articles** to reduce redundancy.
3.  **Recommending personalized news articles** to users based on their reading history, using a novel graph-based approach.

## ✨ Features

*   **Web Scraping:** Fetches news articles from multiple Nepali news sources.
*   **Content Extraction:** Extracts the main content from the articles.
*   **News Clustering:** Groups similar news articles together using machine learning.
*   **Graph-Based Recommendation:** Creates a graph of users and articles to provide insightful recommendations.
*   **API Server:** Exposes endpoints to access the aggregated and recommended news.

## ⚙️ System Architecture

The system is designed with a modular architecture:

1.  **Scraper:** The `scraper` module fetches news articles.
2.  **Clustering:** The `clustering` module processes the articles and groups them based on content similarity.
3.  **Graphing:** The `graphing` module builds a graph that connects users to the news clusters they have interacted with.
4.  **Recommendation:** The `recommendation` module uses this graph to generate personalized news recommendations.
5.  **Server:** A Flask server (`server.py`) provides an API to interact with the system.
6.  **Database:** The `db` module handles all database interactions.
7.  **Firebase:** The `firebase` module is used for user authentication and data storage.

## 🚀 Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

*   Python 3.9 (Minimum)
*   pip

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/mukulboro/graph-news-recommender.git
    cd graph-news-recommender
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## ▶️ Usage

The main entry points for the application are `main.py` and `server.py`.

*   To run the complete pipeline (scraping, clustering, etc.), execute:
    ```sh
    python main.py
    ```

*   To start the API server, run:
    ```sh
    python server.py
    ```

## 📂 Project Structure

```
.
├── clustering/         # Contains the code for news clustering
├── db/                 # Database connection and management
├── firebase/           # Firebase integration
├── graphing/           # Graph creation and analysis
├── news_threading/     # Manages news threads
├── recommendation/     # Recommendation engine logic
├── scraper/            # News scraping scripts
├── .gitignore
├── README.md
├── graph_analysis.py   # Script for analyzing the graph
├── idea                # Project metadata
├── main.py             # Main script to run the pipeline
├── requirements.txt    # Project dependencies
└── server.py           # Flask API server
```

## 🛠️ Technology Stack

*   **Backend:** Python
*   **API:** Flask
*   **Libraries:**
    *   `scikit-learn`: For machine learning and clustering.
    *   `networkx`: For creating and analyzing graphs.
    *   `BeautifulSoup4`: For web scraping.
    *   `requests`: For making HTTP requests.
    *   `firebase-admin`: For Firebase integration.

## 📜 Research Paper

This project is based on the research paper: "A Novel Approach To News Aggregation and Recommendation Using Clustering Algorithms and Graph Theory."

You can read the abstract here: [researchgate.net/publication/392532767_A_Novel_Approach_To_News_Aggregation_and_Recommendation_Using_Clustering_Algorithms_and_Graph_Theory](https://www.researchgate.net/publication/392532767_A_Novel_Approach_To_News_Aggregation_and_Recommendation_Using_Clustering_Algorithms_and_Graph_Theory)

## 🙏 Acknowledgements

*   Nepali Stopwords courtesy of [prtx/Nepali-Stopwords](https://github.com/prtx/Nepali-Stopwords/blob/master/nepali_stopwords.txt).
