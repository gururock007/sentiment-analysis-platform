# core/pipeline.py
import joblib
import re
from core.config import settings

class InferenceEngine:
    def __init__(self):
        print("Loading ML models into worker memory...")
        self.model = joblib.load(settings.MODEL_PATH)
        self.vectorizer = joblib.load(settings.VECTORIZER_PATH)
        print("Model and Vectorizer loaded successfully!")

    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return " ".join(text.split())

    def predict(self, raw_text: str):
        cleaned = self.clean_text(raw_text)
        # If text is empty after cleaning, fallback to avoid vectorizer crashes
        if not cleaned.strip():
            return "Negative", 0.50

        features = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(features)[0]
        probability = self.model.predict_proba(features)[0][prediction]
        
        sentiment = "Positive" if prediction == 1 else "Negative"
        return sentiment, float(probability)