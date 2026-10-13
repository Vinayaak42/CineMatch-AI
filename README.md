# 🎬 CineMatch AI — Intelligent Movie Recommendation System


CineMatch AI is a machine-learning-powered movie recommendation platform that helps users discover movies based on their interests, genres, ratings, and viewing preferences.

Built with Python and Streamlit, the application combines content-based recommendation techniques, movie search, movie information from The Movie Database (TMDB), data analytics, and personalized recommendations in an interactive web interface.

The project demonstrates practical applications of **machine learning, natural language processing, data analysis, recommendation systems, API integration, and application development**.

---

## 📌 Table of Contents

* [Project Overview](#-project-overview)
* [Key Features](#-key-features)
* [Application Modules](#-application-modules)
* [Technology Stack](#-technology-stack)
* [System Architecture](#-system-architecture)
* [Recommendation Methodology](#-recommendation-methodology)
* [Dataset](#-dataset)
* [Project Structure](#-project-structure)
* [Installation and Setup](#-installation-and-setup)
* [TMDB API Configuration](#-tmdb-api-configuration)
* [Run the Application](#-run-the-application)
* [How to Use CineMatch AI](#-how-to-use-cinematch-ai)
* [Model Training](#-model-training)
* [Testing](#-testing)
* [Evaluation and Limitations](#-evaluation-and-limitations)
* [Deployment](#-deployment)
* [Security and Privacy](#-security-and-privacy)
* [Future Improvements](#-future-improvements)
* [Learning Outcomes](#-learning-outcomes)
* [Author](#-author)
* [License](#-license)

---

## 🚀 Project Overview

Choosing a movie can be difficult when thousands of titles are available across different genres and categories.

CineMatch AI addresses this problem by analyzing movie metadata and identifying titles with similar characteristics.

The application uses a content-based recommendation approach to compare movie descriptions represented through their titles and genres. TF-IDF vectorization transforms this text into numerical features, and cosine similarity measures how closely movies match one another.

The platform also provides movie exploration, external movie search, analytics, and user-specific recommendation features.

### Project Goals

* Build an interactive movie recommendation application.
* Apply machine learning techniques to movie metadata.
* Implement text preprocessing and feature extraction.
* Generate movie recommendations using similarity scores.
* Integrate an external movie information API.
* Analyze movie and rating datasets.
* Store user ratings and watchlists using SQLite.
* Develop a portfolio-ready data science application.

---

## ✨ Key Features

### 1. 🏠 Home Dashboard

Provides an overview of the movie dataset and the application's capabilities.

Features include:

* Movie catalog overview.
* Rating dataset statistics.
* Popular movie discovery.
* Navigation to recommendation and analytics modules.

### 2. 🔍 Movie Exploration

Allows users to explore the available movie catalog.

Features include:

* Search movies by title.
* Explore available genres.
* Inspect movie metadata.
* Filter and browse movie selections.

### 3. 🤖 AI Movie Recommendations

Recommends movies similar to a selected movie using content-based filtering.

The recommendation pipeline includes:

1. Movie metadata preprocessing.
2. Text feature construction.
3. TF-IDF vectorization.
4. Cosine similarity calculation.
5. Ranking candidate movies.
6. Returning the highest-ranked recommendations.

Users can discover movies with similar genres and title characteristics.

### 4. 🌐 Live Movie Search

Integrates with The Movie Database (TMDB) API to search for movie information.

Depending on API availability and the implemented interface, users can explore:

* Movie titles.
* Posters.
* Release dates.
* Descriptions.
* Ratings.
* Additional movie information.

TMDB provides external movie information; its movie identifiers should not be confused with MovieLens movie IDs.

### 5. 🔥 Popular Movies

Provides access to popular movie listings retrieved through TMDB.

This feature complements the local MovieLens-based recommendation engine with external movie discovery.

### 6. 📊 Data Analytics

Provides an overview of the movie and rating datasets.

Potential analytical views include:

* Genre distribution.
* Rating distribution.
* Most frequently rated movies.
* Highest-rated movies subject to minimum rating-count thresholds.
* Release-year distribution.
* Rating and catalog statistics.

These analyses help demonstrate exploratory data analysis (EDA) and data visualization skills.

### 7. 🧹 Data Quality Analysis

Supports inspection of the underlying datasets.

Data quality checks may include:

* Missing values.
* Duplicate records.
* Invalid rating values.
* Movie identifier consistency.
* Data shape and column summaries.
* Cleaning and preprocessing results.

### 8. 👤 Personalized Recommendations

Uses a user's saved movie ratings to generate recommendations based on their preferences.

The personalized recommendation module considers positive and negative rating signals and combines them with movie similarity scores.

The results depend on the available rating history and the recommendation logic implemented in the application.

### 9. ⭐ Movie Rating System

Allows users to save ratings for movies.

User ratings are stored locally using SQLite and can be used to improve the relevance of personalized recommendations.

### 10. ❤️ Watchlist Management

Allows users to maintain a list of movies they want to watch.

The application stores watchlist entries in the local database and provides functionality to view and manage them.

---

## 🧩 Application Modules

| Module               | Description                                    |
| -------------------- | ---------------------------------------------- |
| Home                 | Application overview and dataset statistics    |
| Explore Movies       | Search and explore the movie catalog           |
| AI Recommendations   | Content-based movie recommendations            |
| Live TMDB Search     | Search for movies using the TMDB API           |
| Popular Movies       | Discover popular movies from TMDB              |
| Data Analytics       | Explore movie and rating distributions         |
| Data Quality         | Inspect data quality and preprocessing         |
| Personalized For You | Generate recommendations from user preferences |
| Rate Movies          | Save and manage movie ratings                  |
| My Watchlist         | View and manage saved movies                   |

The availability of individual features depends on the application code and its configuration.

---

## 🛠️ Technology Stack

### Programming Language

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* TF-IDF Vectorization
* Cosine Similarity
* Content-Based Filtering

### Web Application

* Streamlit

### Data Visualization

* Plotly
* Pandas visualization

### API Integration

* Requests
* The Movie Database (TMDB) API

### Database

* SQLite
* SQL

### Model Persistence

* Joblib

### Testing

* Pytest

### Development Tools

* Git
* GitHub
* Visual Studio Code
* PowerShell

---

## 🏗️ System Architecture

```text
                 ┌───────────────────────────┐
                 │       MovieLens Data      │
                 │   Movies and Ratings CSV  │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │    Data Preprocessing     │
                 │ Cleaning and Validation   │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │   Feature Engineering     │
                 │  Movie Titles and Genres  │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │      TF-IDF Model         │
                 │ Text Feature Extraction   │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │   Cosine Similarity       │
                 │ Movie Similarity Ranking  │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │   Recommendation Engine   │
                 └─────────────┬─────────────┘
                               │
                               ▼
                 ┌───────────────────────────┐
                 │     Streamlit Interface   │
                 │ Search, Explore, Suggest  │
                 └───────────────────────────┘
```

### Supporting Components

The main recommendation pipeline is supported by:

* TMDB API integration for external movie information.
* SQLite for locally stored user ratings and watchlists.
* Pandas for data analysis and reporting.
* Joblib for saving and loading the trained recommendation model.

---

## 🧠 Recommendation Methodology

CineMatch AI uses content-based filtering.

Unlike collaborative filtering, which learns from similarities between users and their interactions, content-based filtering recommends items based on the characteristics of the items themselves.

### Step 1: Data Preprocessing

The preprocessing pipeline prepares the movie and rating datasets.

Typical operations include:

* Removing duplicate movie identifiers.
* Handling missing movie titles.
* Cleaning genre information.
* Extracting release years from titles when available.
* Removing duplicate user-movie ratings.
* Validating rating values.
* Ensuring that ratings refer to known movies.

### Step 2: Feature Construction

Movie titles and genres are converted into a text representation.

The feature text combines cleaned movie titles with genre information.

Genre information can be repeated in the feature text to give it additional influence during vectorization.

### Step 3: TF-IDF Vectorization

Term Frequency–Inverse Document Frequency (TF-IDF) converts movie text into numerical vectors.

TF-IDF helps represent terms according to their importance within the collection of movie records.

The implementation can use:

* English stop-word removal.
* Unigrams and bigrams.
* Sparse feature representations.
* A configurable maximum vocabulary size.

### Step 4: Cosine Similarity

Cosine similarity measures the similarity between numerical feature vectors.

The similarity between vectors \(A\) and \(B\) is:

$$
\operatorname{similarity}(A,B)
=
\frac{A \cdot B}{\|A\|\|B\|}
$$

Higher scores indicate greater alignment between the feature vectors.

### Step 5: Recommendation Ranking

The recommendation engine:

1. Identifies the selected movie.
2. Compares it with other movies.
3. Calculates similarity scores.
4. Excludes the selected movie from the results.
5. Ranks candidates by similarity.
6. Returns the requested number of recommendations.

### Step 6: Personalized Ranking

The personalized module uses saved user ratings as preference signals.

Movies that resemble highly rated titles can receive a stronger recommendation signal, while movies resembling poorly rated titles can receive a weaker signal.

The effectiveness of this approach depends on the user's rating history and the implemented scoring strategy.

---

## 📁 Dataset

CineMatch AI uses the MovieLens dataset.

### Dataset Source

**Official dataset download:**

https://files.grouplens.org/datasets/movielens/ml-latest-small.zip

**MovieLens website:**

https://movielens.org/

### Dataset Files

The `ml-latest-small` dataset includes:

| File          | Description                                                    |
| ------------- | -------------------------------------------------------------- |
| `movies.csv`  | Movie IDs, titles, and genres                                  |
| `ratings.csv` | User IDs, movie IDs, ratings, and timestamps                   |
| `tags.csv`    | User-generated movie tags                                      |
| `links.csv`   | External movie identifiers, including TMDB IDs where available |

The `movies.csv` and `ratings.csv` files are the primary inputs for the core recommendation pipeline.

The small dataset contains approximately 9,700 movies and 100,000 ratings. Exact counts may vary with the dataset version.

### Expected Local Data Structure

```text
data/
├── movies.csv
├── ratings.csv
├── cleaned_movies.csv
└── cleaned_ratings.csv
```

The cleaned files are generated by the preprocessing pipeline if the application is configured to save them.

### Download and Extract the Dataset

1. Download the ZIP file from the official GroupLens URL.
2. Extract its contents.
3. Copy `movies.csv` and `ratings.csv` into the project's `data/` directory.
4. Confirm that the filenames match the paths expected by the application.

---

## 📂 Project Structure

The repository is organized into separate modules for data preparation, recommendation logic, API integration, the user interface, and user data storage.

```text
CineMatch-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── cleaned_movies.csv
│   ├── cleaned_ratings.csv
│   └── cinematch.db
│
├── models/
│   └── movie_recommender.joblib
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── analytics.py
│   ├── recommender.py
│   ├── train_model.py
│   ├── tmdb_client.py
│   ├── ui.py
│   ├── user_store.py
│   ├── personalized.py
│   └── profile_ui.py
│
├── tests/
│   ├── test_recommender.py
│   └── test_user_store.py
│
└── .streamlit/
    └── config.toml
```

**Note:** This structure represents the intended organization. Some files, generated artifacts, or tests may be absent from a particular checkout. The local SQLite database and trained model can be generated by the application, depending on its configuration.

---

## 💻 Installation and Setup

### Prerequisites

Install the following:

* Python 3.10 or a compatible version supported by your dependencies.
* Git.
* A GitHub account if you intend to publish the project.
* A TMDB API key for live movie search features.

Check your Python installation:

```bash
python --version
```

Check Git:

```bash
git --version
```

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vinayaak42/CineMatch-AI.git
```

Move into the project directory:

```bash
cd CineMatch-AI
```

### Step 2: Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can invoke the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip --version
```

### Step 3: Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project's dependencies:

```powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` does not yet exist or is incomplete, create it based on the libraries imported by the actual project modules.

### Step 4: Prepare the Dataset

Download the MovieLens dataset from:

https://files.grouplens.org/datasets/movielens/ml-latest-small.zip

Extract the archive and place `movies.csv` and `ratings.csv` in the `data/` directory.

### Step 5: Configure the API

Create a `.env` file in the project root if your local TMDB client uses environment variables.

Example:

```env
TMDB_API_KEY=your_tmdb_api_key
```

Replace the placeholder with your own key. Never commit this file to GitHub.

---

## 🔑 TMDB API Configuration

CineMatch AI uses The Movie Database (TMDB) API for external movie search and information.

### Obtain an API Key

Visit the official TMDB website:

https://www.themoviedb.org/

Create an account and follow the developer instructions to obtain an API key or read access token.

### Local Configuration

If your application uses `python-dotenv`, place the key in `.env`:

```env
TMDB_API_KEY=your_tmdb_api_key
```

The application may also support `TMDB_READ_ACCESS_TOKEN`, depending on the implementation in `src/tmdb_client.py`.

### Deployment Configuration

When deploying to Streamlit Community Cloud, add the required secret through the app's secrets settings.

For example, if the code reads `TMDB_API_KEY`:

```toml
TMDB_API_KEY = "your_tmdb_api_key"
```

Use the environment variable name expected by your code. Do not publish real API credentials in this README, source files, screenshots, or Git commits.

### TMDB Attribution

This product uses the TMDB API but is not endorsed or certified by TMDB.

Refer to the official documentation:

https://developer.themoviedb.org/docs

---

## ▶️ Run the Application

From the project root, activate the virtual environment and run:

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal, typically:

```text
http://localhost:8501
```

Open the displayed URL in your browser.

To stop the application, press `Ctrl+C` in the terminal.

---

## 🎯 How to Use CineMatch AI

### Discover Similar Movies

1. Launch the application.
2. Open the AI Recommendations section.
3. Search for or select a movie.
4. Generate recommendations.
5. Explore the returned movie titles and similarity scores.

### Search for Movies

1. Open Live TMDB Search.
2. Enter a movie title.
3. Submit the search.
4. Explore the returned movie information.

Live search requires a valid TMDB API configuration and an available internet connection.

### Explore Analytics

1. Open Data Analytics.
2. Review the available charts and statistics.
3. Compare genres, ratings, and other supported distributions.

### Save Personal Ratings

1. Select or create a local user profile.
2. Open Rate Movies.
3. Select a movie and submit a rating.
4. Review your saved rating history.

### Manage a Watchlist

1. Open My Watchlist.
2. Add movies you want to watch.
3. Review or remove saved entries.

### Generate Personalized Recommendations

1. Save ratings for several movies.
2. Open Personalized For You.
3. Generate recommendations.
4. Explore the results based on your rating history.

Recommendations may be less meaningful when a user has very few saved ratings.

---

## 🏋️ Model Training

The recommendation model can be trained using the project's training module or through the application's model-loading logic, depending on the implementation.

If `src/train_model.py` supports direct execution, use:

```powershell
python -m src.train_model
```

The expected model artifact location is:

```text
models/movie_recommender.joblib
```

The recommender may also be trained automatically if the expected saved model does not exist.

### Model Persistence

Joblib allows Python objects to be saved and loaded from disk.

Persisting the fitted TF-IDF vectorizer, movie metadata, and recommendation model state can reduce repeated training during application startup.

**Important:** The exact training command and output depend on the implementation in `src/train_model.py`. Confirm that the module supports direct execution before using the command above.

---

## 🧪 Testing

The repository may include automated tests for recommendation logic and user data storage.

Run the test suite with:

```powershell
python -m pytest tests -v
```

Check Python syntax:

```powershell
python -m py_compile app.py
```

Compile the source modules:

```powershell
python -m compileall src
```

These commands help identify syntax errors and test failures before deployment.

A successful syntax check does not guarantee that the application will run correctly: API configuration, missing datasets, dependency mismatches, and runtime errors must also be tested.

---

## 📈 Evaluation and Limitations

### Evaluation Approach

The recommendation engine can be evaluated through:

* Manual inspection of recommendations for selected movies.
* Relevance of recommended genres and titles.
* Diversity of recommended results.
* Response time for movie searches and recommendation generation.
* User feedback.
* Offline ranking metrics when suitable ground-truth data is available.

Possible offline recommendation metrics include Precision@K, Recall@K, NDCG@K, and catalog coverage.

These metrics should be reported only after a suitable evaluation procedure has been implemented and executed.

### Current Limitations

#### 1. Limited Movie Features

If recommendations rely primarily on titles and genres, the model cannot fully understand plot, themes, actors, directors, or nuanced viewer preferences.

#### 2. Cold-Start Problem

New users have limited rating history. New movies may also be difficult to recommend without sufficient metadata.

#### 3. Popularity and Relevance

Similarity-based recommendations are not necessarily the most popular or highest-rated movies.

#### 4. Dataset Coverage

The local MovieLens catalog may not contain every movie returned by TMDB.

#### 5. API Dependency

Live movie search depends on TMDB availability, valid credentials, and network access.

#### 6. Local Persistence

SQLite data is stored locally unless the application is configured to use a persistent external database.

#### 7. Evaluation

The usefulness of recommendations should be measured through appropriate offline metrics and user feedback rather than assumed from similarity scores alone.

---

## ☁️ Deployment

CineMatch AI can be deployed using Streamlit Community Cloud.

### Deployment Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the `Vinayaak42/CineMatch-AI` repository.
5. Select the `main` branch.
6. Set the application entry point to `app.py`.
7. Configure the required TMDB secrets.
8. Deploy the application.
9. Check the deployment logs if startup fails.

**Streamlit Community Cloud:**

https://streamlit.io/cloud

### Deployment Checklist

* Confirm that `app.py` exists at the repository root.
* Ensure all imported modules are included.
* Include a complete `requirements.txt`.
* Configure secrets outside the source code.
* Ensure required datasets are available.
* Ensure required model files are included or can be generated.
* Test the app without relying on files that exist only on your local machine.
* Check file-size limits before uploading large artifacts.
* Verify whether SQLite persistence meets your needs.

For a multi-user production deployment, consider using a managed database instead of relying on a local SQLite file.

---

## 🔐 Security and Privacy

The project should follow these security practices:

* Never commit API keys or passwords.
* Store credentials in environment variables or deployment secrets.
* Exclude `.env` and virtual environments from version control.
* Avoid committing personal or sensitive data.
* Validate user inputs.
* Handle external API errors safely.
* Avoid exposing sensitive exception details to end users.
* Review generated files before publishing the repository.

The current SQLite profile functionality is intended for local application use. Unless authentication and authorization have been implemented, profiles should not be treated as secure user accounts.

---

## 🔮 Future Improvements

CineMatch AI can be extended with additional data science and software engineering capabilities.

### Recommendation Improvements

* Hybrid recommendation combining content-based and collaborative filtering.
* User-item matrix factorization.
* Implicit feedback from watchlists and interactions.
* Better cold-start handling.
* Personalized ranking and recommendation diversity.
* Explanation of why each movie was recommended.

### Natural Language Processing

* Movie plot embeddings.
* Semantic search.
* Transformer-based text representations.
* Natural-language movie discovery.

### Data Engineering

* Automated data ingestion.
* Scheduled dataset refreshes.
* Data validation pipelines.
* Improved logging and error handling.

### MLOps

* MLflow experiment tracking.
* Recommendation model versioning.
* Reproducible training runs.
* Automated evaluation.
* Model performance monitoring.

### Deployment and Scalability

* Managed PostgreSQL storage.
* User authentication.
* FastAPI recommendation endpoints.
* Docker-based deployment.
* Continuous integration and testing.
* Cloud hosting and monitoring.

These are potential improvements and should not be considered completed features until implemented.

---

## 🎓 Learning Outcomes

This project provides practical experience with:

* Python application development.
* Exploratory data analysis.
* Data cleaning and preprocessing.
* Feature engineering.
* TF-IDF text vectorization.
* Cosine similarity.
* Content-based recommendation systems.
* Machine learning model persistence.
* REST API integration.
* Streamlit application development.
* SQL and SQLite data storage.
* Data visualization.
* Automated testing.
* Git and GitHub version control.
* Application deployment.

---

## 👨‍💻 Author

**Vinayak Kesti**

Aspiring Data Scientist | Data Analyst | AI/ML Engineer

Interested in machine learning, recommendation systems, data analytics, NLP, and production-oriented AI applications.

* **GitHub:** https://github.com/Vinayaak42
* **LinkedIn:** https://www.linkedin.com/in/vinayak-kesti/

---

## 📄 License

This project is intended for educational and portfolio purposes.

A license has not been specified for this repository. If you intend to permit others to use, modify, and distribute the code, consider adding an appropriate open-source license file.

The MovieLens dataset and TMDB services are subject to their respective terms and policies. Refer to their official websites for details.

---

## ⭐ Support the Project

If you find CineMatch AI useful or interesting, consider starring the repository on GitHub.

Feedback, suggestions, and ideas for improving the recommendation experience are welcome.

**Thank you for exploring CineMatch AI!** 🍿
