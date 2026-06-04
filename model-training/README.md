```markdown
# Sentiment Analyzer

A modular, production-ready machine learning pipeline for text sentiment analysis. This project utilizes the **Sentiment140 dataset** (1.6 million tweets) to train a highly efficient TF-IDF and Logistic Regression baseline classifier.

## 📁 Project Structure

```text
.
├── config
│   └── config.yml       # Data paths and model hyper-parameters
├── datasets
│   ├── processed        # Train/test split artifacts (git-ignored)
│   ├── raw              # Raw data sources (Sentiment140)
│   └── samples          # Small batches for quick inference testing
├── main.py              # Interactive command-line analyzer
├── models               # Saved binaries (.pkl) for model & vectorizer
├── pyproject.toml       # Project metadata, dependencies, and shortcuts
├── README.md            # Project documentation
└── scripts
    ├── evaluate.py      # Computes accuracy, precision, recall, and F1-score
    ├── predict.py       # Core prediction engine utility
    ├── preprocess.py    # Cleans text, normalizes targets, handles train/test split
    └── train.py         # Extracts TF-IDF features and trains the classifier

```

---

## 📊 Dataset Context (Sentiment140)

The model is built around the `training.1600000.processed.noemoticon.csv` file. The ingestion pipeline automatically accounts for the dataset's standard quirks:

* **Encoding:** Loaded using `latin-1` to parse social media characters.
* **Format:** Lacks a header row (columns are programmatically mapped).
* **Target Labels:** Original targets `0` (Negative) and `4` (Positive) are re-mapped to a standard binary standard of `0` and `1`.

---

## ⚙️ Setup & Installation

This project manages dependencies and execution scripts via `pyproject.toml`.

### Prerequisites

Ensure you have Python 3.10+ installed. Place the raw dataset inside the `datasets/raw/` directory before starting.

### Install via Poetry

```bash
# Install dependencies and spin up the virtual environment
poetry install

```

---

## 🚀 Running the Pipeline

You can run the entire machine learning pipeline sequentially using the custom shortcut scripts defined in `pyproject.toml`.

### 1. Data Preprocessing

Cleans text (removes URLs, handles `@mentions`, and non-alphabetical noise), standardizes target fields, and creates stratified train/test files.

```bash
poetry run preprocess

```

### 2. Model Training

Extracts unigram and bigram TF-IDF features (up to 50,000 maximum features) and trains a Logistic Regression classifier using parallel CPU processing.

```bash
poetry run train

```

### 3. Evaluation

Evaluates model performance against the unseen test partition and prints a detailed scikit-learn classification report.

```bash
poetry run evaluate

```

### 4. Interactive Testing

Launch the interactive command-line interface to check custom strings and real-time confidence scores.

```bash
poetry run analyze

```

---

## 🛠️ Configuration Changes

To tweak the train/test split balance, filter out different feature limits, or alter model regularization metrics, adjust the values directly inside `config/config.yml` without modifying core script code.

```

```