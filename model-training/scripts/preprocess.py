import pandas as pd
import re
import yaml
from sklearn.model_selection import train_test_split

def load_config():
    with open("config/config.yml", "r") as f:
        return yaml.safe_load(f)

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove user handles (@user)
    text = re.sub(r'@\w+', '', text)
    # Remove website links
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove special characters and numbers, keep only letters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Collapse multiple spaces into one
    return " ".join(text.split())

def preprocess_data():
    config = load_config()
    print("Loading Sentiment140 dataset...")
    
    # Sentiment140 has 6 columns, no header. 
    # Col 0: target, Col 5: text
    df = pd.read_csv(
        config['paths']['raw_data'], 
        encoding='latin-1', 
        header=None, 
        usecols=[0, 5], 
        names=['target', 'text']
    )
    
    print("Cleaning tweets (this might take a minute)...")
    df['text'] = df['text'].apply(clean_text)
    
    # Map target: 0 stays 0 (negative), 4 becomes 1 (positive)
    df['target'] = df['target'].map({0: 0, 4: 1})
    
    # Drop any rows that became empty after cleaning
    df = df[df['text'].str.strip() != ""]
    
    print("Splitting into train and test sets...")
    train_df, test_df = train_test_split(
        df, 
        test_size=config['data_params']['test_size'], 
        random_state=config['data_params']['random_state'],
        stratify=df['target']
    )
    
    train_df.to_csv(config['paths']['processed_train_data'], index=False)
    test_df.to_csv(config['paths']['processed_test_data'], index=False)
    print("Preprocessing complete! Files saved to datasets/processed/")

if __name__ == "__main__":
    preprocess_data()