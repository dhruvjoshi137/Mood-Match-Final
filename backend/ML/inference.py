import torch
import os
from transformers import AutoTokenizer
from ML.model import CustomRobertaModel

# CONFIG
model_checkpoint = "roberta-large"
num_labels = 28
pos_weights = [1.0] * num_labels
label_names = [
    "admiration", "amusement", "anger", "annoyance", "approval", "caring",
    "confusion", "curiosity", "desire", "disappointment", "disapproval",
    "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
    "joy", "love", "nervousness", "optimism", "pride", "realization", "relief",
    "remorse", "sadness", "surprise", "neutral"
]

def get_model_and_tokenizer():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, clean_up_tokenization_spaces=True)
    print("Loading model architecture...")
    model = CustomRobertaModel(model_checkpoint, num_labels, pos_weights)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "pytorch_model.bin")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    print("Loading model weights...")
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    print("Model ready.")
    return model, tokenizer

# Predict function
def predict_emotion(text, threshold=0.5):
    model, tokenizer = get_model_and_tokenizer()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(device)

    try:
        with torch.no_grad():
            outputs = model(**inputs)
            # Support both dict and tuple output
            if isinstance(outputs, dict):
                logits = outputs.get("logits", None)
            elif isinstance(outputs, tuple):
                logits = outputs[0]
            else:
                logits = None
            if logits is None:
                print("[ML DEBUG] Model output missing logits. Output:", outputs)
                return ["neutral"], "neutral"
            probs = torch.sigmoid(logits).cpu().numpy()[0]
    except Exception as e:
        print(f"[ML DEBUG] Model inference error: {e}")
        return ["neutral"], "neutral"

    print("[ML DEBUG] Raw model probabilities:", probs)
    predicted_labels = []
    max_prob = 0
    dominant_label = "neutral"
    for i, prob in enumerate(probs):
        if prob >= threshold:
            predicted_labels.append(label_names[i])
        if prob > max_prob:
            max_prob = prob
            dominant_label = label_names[i]

    print("[ML DEBUG] Predicted labels:", predicted_labels)
    print("[ML DEBUG] Dominant label:", dominant_label)
    # Always return a valid label
    if not dominant_label:
        dominant_label = "neutral"
    if not predicted_labels:
        predicted_labels = [dominant_label]
    return predicted_labels, dominant_label
