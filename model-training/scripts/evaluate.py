import pandas as pd
import yaml
import joblib
from sklearn.metrics import classification_report, accuracy_score

def load_config():
    with open("config/config.yml", "r") as f:
        return yaml.safe_load(f)

def evaluate_model():
    config = load_config()
    print("Loading test data and model...")
    test_df = pd.read_csv(config['paths']['processed_test_data']).dropna()
    
    model = joblib.load(config['paths']['model_path'])
    vectorizer = joblib.load(config['paths']['vectorizer_path'])
    
    X_test = vectorizer.transform(test_df['text'])
    y_test = test_df['target']
    
    print("Running predictions...")
    predictions = model.predict(X_test)
    
    print("\n--- Evaluation Results ---")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}\n")
    print(classification_report(y_test, predictions, target_names=['Negative', 'Positive']))

if __name__ == "__main__":
    evaluate_model()