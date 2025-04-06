# Install transformers and torch if not installed
# pip install transformers torch pandas

import torch
from transformers import BertTokenizer, BertModel
import pandas as pd

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')


df = pd.read_csv(r'C:\Users\HP\Downloads\geographical_features_data3.csv')  # Modify this line according to your dataset's format
texts = df['Title'].tolist()    # Assuming there's a 'text_column' in your dataset

# Create a function to extract BERT features for each text in the dataset
def extract_bert_features(texts):
    features = []
    
    for text in texts:
        # Tokenize input text
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        
        # Perform feature extraction using BERT embeddings
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Extract the last hidden states (embeddings) for each token
        embeddings = outputs.last_hidden_state
        
        # For simplicity, we'll use the [CLS] token embedding (first token) as the sentence embedding
        sentence_embedding = embeddings[:, 0, :].squeeze().numpy()  # Extracting the first token ([CLS] token)
        
        features.append(sentence_embedding)
    
    return features

# Extract features for the entire dataset
bert_features = extract_bert_features(texts)

# You can convert it into a DataFrame or save the features for later use
features_df = pd.DataFrame(bert_features)
features_df.to_csv('feature.csv', index=False)  # Saving the features as CSV
