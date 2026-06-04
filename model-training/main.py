# main.py
import sys
from scripts.predict import get_predictor

def main():
    try:
        predict_fn = get_predictor()
    except FileNotFoundError:
        print("Error: Model files not found. Please run the training pipeline first.")
        sys.exit(1)
        
    print("\n=== Sentiment Analyzer Initialized ===")
    print("Type a sentence to analyze its sentiment (or type 'exit' to quit).\n")
    
    while True:
        user_input = input("Enter text: ")
        if user_input.lower() == 'exit':
            break
            
        if not user_input.strip():
            continue
            
        sentiment, confidence = predict_fn(user_input)
        print(f"Result: {sentiment} ({confidence*100:.1f}% confidence)\n")

if __name__ == "__main__":
    main()