from colorama import Fore, Style
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple
import colorama

# Parallelizes tasks to make them less CPU-intensive
device = "cuda:0" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]


def estimate_sentiment(news, verbose=False, symbol = ""):
    if news:
        if verbose:
            print(f"{Fore.LIGHTMAGENTA_EX}\nHeadlines: {symbol}{Style.RESET_ALL}")
            for new in news:
                print(new)
        # Tokenize the news headlines
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)
        # Pass tokens through the model
        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
        # Calculate softmax probabilities
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        # Get the highest probability and corresponding sentiment
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        if verbose:
            print("\nCouldn't find symbol.")
        return 0, labels[-1]

