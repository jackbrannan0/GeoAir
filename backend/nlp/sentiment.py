from transformers import pipeline
import torch
device = 0 if torch.mps.is_available() else -1
classifier = pipeline("sentiment-analysis"
                      ,model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                      device=device)

async def analyze_sentiment(text):
    result = classifier(text)[0]
    
    # Logic: Get the label with the highest score
    label = result['label']
    score = result['score']
    
    return label, score

