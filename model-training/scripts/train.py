import pandas as pd
import yaml
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def load_config():
    with open("config/config.yml", "r") as f:
        return yaml.safe_load(f)

def train_model():
    config = load_config()
    print("Loading processed training data...")
    train_df = pd.read_csv(config['paths']['processed_train_data']).dropna()
    
    print("Vectorizing text using TF-IDF...")
    # ngram_range=(1,2) extracts both single words and two-word phrases
    vectorizer = TfidfVectorizer(max_features=50000, ngram_range=(1, 2))
    X_train = vectorizer.fit_transform(train_df['text'])
    y_train = train_df['target']
    
    print("Training Logistic Regression model...")
    model = LogisticRegression(
        max_iter=config['model_params']['max_iter'], 
        C=config['model_params']['C'],
        n_jobs=-1 # Uses all available CPU cores
    )
    model.fit(X_train, y_train)
    
    print("Saving model and vectorizer...")
    joblib.dump(model, config['paths']['model_path'])
    joblib.dump(vectorizer, config['paths']['vectorizer_path'])
    print("Training complete! Model saved to models/")

if __name__ == "__main__":
    train_model()