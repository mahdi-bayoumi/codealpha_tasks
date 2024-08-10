from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Define the model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Sample text for sentiment analysis
text = "This movie was absolutely fantastic!"

# Tokenize the text
encoded_text = tokenizer(text, return_tensors="pt")  # Convert to PyTorch tensors

# Perform sentiment classification (assuming the model has labels for sentiment)
with torch.no_grad():
    outputs = model(**encoded_text)
    predictions = torch.argmax(outputs.logits, dim=-1)  # Get the predicted class

# Print the predicted sentiment label (modify based on your model's labels)
if predictions.item() == 0:
    print("Negative sentiment")
elif predictions.item() == 1:
    print("Positive sentiment")
else:
    print("Neutral sentiment")