# scripts/predict.py
import yaml
import joblib

def load_config():
    with open("config/config.yml", "r") as f:
        return yaml.safe_load(f)

def get_predictor():
    config = load_config()
    model = joblib.load(config['paths']['model_path'])
    vectorizer = joblib.load(config['paths']['vectorizer_path'])
    
    def predict(text):
        X = vectorizer.transform([text])
        prediction = model.predict(X)[0]
        # Calculate probability for cleaner output
        prob = model.predict_proba(X)[0][prediction]
        sentiment = "Positive" if prediction == 1 else "Negative"
        return sentiment, prob
        
    return predict