import re
import torch
import torch.nn as nn
import emoji
import os
import torch.nn.functional as F
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
import requests 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
text_processor = TextPreProcessor(
    normalize=[],       # nothing else
    annotate=[],        # no annotation
    fix_html=False,
    tokenizer=None,     # don't tokenize
    dicts=[emoticons]
)
url = "https://gist.githubusercontent.com/behitek/7d9441c10b3c2739499fc5a4d9ea06fb/raw/db0b7e2f1b27c68fcdc596e2049deac23777219b/teencode.txt"
text = requests.get(url).text

slang_dict = {}

for line in text.strip().split("\n"):
    parts = line.split()
    key = parts[0]
    value = " ".join(parts[1:])
    slang_dict[key] = value
def data_preprocess(text):

    # Demojize emojis
    cleaned = emoji.demojize(text)

    cleaned = text_processor.pre_process_doc(cleaned)

    cleaned = re.sub(r":(\w+):|<(\w+)>", lambda match: f"<e>{match.group(1) or match.group(2)}</e>", cleaned)

    words = cleaned.split()
    new_words = []
    for w in words:
        if w in slang_dict:
            new_words.append(slang_dict[w])
        else:
            new_words.append(w)
    return " ".join(new_words)

checkpoint_path = os.path.join(BASE_DIR, "analyzer", "checkpoint.pth")
model_name = "distilbert-base-multilingual-cased"
device = torch.device("cpu")

# -------------------------
# Load tokenizer
# -------------------------
tokenizer = AutoTokenizer.from_pretrained(model_name)

# If you added custom tokens during training:
new_tokens = ["<e>", "</e>"]
tokenizer.add_tokens(new_tokens)

# -------------------------
# Load model
# -------------------------
print("Loading base model...")
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3
)

# Resize embeddings for added tokens
model.resize_token_embeddings(len(tokenizer))

# -------------------------
# Load checkpoint (handling DataParallel keys)
# -------------------------
print("Loading checkpoint:", checkpoint_path)
checkpoint = torch.load(checkpoint_path, map_location=device)

state_dict = checkpoint["model_state_dict"]
# Strip "module." prefix if it exists
new_state_dict = {k.replace("module.", ""): v for k, v in state_dict.items()}

model.load_state_dict(new_state_dict)
model.to(device)
model.eval()
print("Model loaded successfully on CPU.")

# -------------------------
# Label mapping
# -------------------------
label_map = {
    0: "Negative",
    1: "Positive",
    2: "Neutral"
}

# -------------------------
# Prediction function
# -------------------------
@torch.no_grad()
def predict_sentiment(text: str):
    if len(text) < 5:
        raise ValueError("Câu không hợp lệ, thử lại")
    if len(text.strip()) >50:
        text= text.strip()[:50]
    text = data_preprocess(text)
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    logits = model(**inputs).logits

    # Convert logits to probability (softmax)
    probs = F.softmax(logits, dim=-1)

    # Get predicted class
    pred = torch.argmax(probs, dim=-1).item()

    # Get confidence score of that predicted class
    confidence = probs[0][pred].item()

    # If confidence < 50%, return neutral (0)
    if confidence < 0.5:
        return label_map[2]  # neutral

    return label_map[pred]