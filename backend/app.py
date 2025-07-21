from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
import json
import spacy
import logging
import torch
import os
import sys

from ML.inference import predict_emotion, label_names
from detect_important import parse_prompt, merge_prompt_with_spec, generate_moodboard


print("Starting app.py...")
app = Flask(__name__)
CORS(app)


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)


# Load design dataset
try:
    design_json_path = os.path.join(os.path.dirname(__file__), 'emotion_design_dataset.json')
    with open(design_json_path, 'r') as f:
        design_data = json.load(f)
except FileNotFoundError:
    logging.error("emotion_design_dataset.json not found")
    raise

# Load best threshold
best_threshold = 0.5

# Load spacy for negation detection
nlp = spacy.load("en_core_web_sm")

# Direct keyword mapping
emotion_mapping = {
    "happy": "JOY/HAPPINESS", "cheerful": "JOY/HAPPINESS", "excited": "JOY/HAPPINESS",
    "fun": "JOY/HAPPINESS", "laughter": "JOY/HAPPINESS", "giggle": "JOY/HAPPINESS",
    "playful": "JOY/HAPPINESS", "amused": "JOY/HAPPINESS", "optimistic": "JOY/HAPPINESS",
    "delighted": "JOY/HAPPINESS", "bubbly": "JOY/HAPPINESS", "bright": "JOY/HAPPINESS",
    "gleeful": "JOY/HAPPINESS", "jubilant": "JOY/HAPPINESS", "energetic": "JOY/HAPPINESS",
    "vibrant": "JOY/HAPPINESS", "sad": "SORROW/DUSK", "sorrow": "SORROW/DUSK",
    "gloomy": "SORROW/DUSK", "down": "SORROW/DUSK", "depressed": "SORROW/DUSK",
    "teary": "SORROW/DUSK", "blue": "SORROW/DUSK", "somber": "SORROW/DUSK",
    "melancholic": "SORROW/DUSK", "heartbroken": "SORROW/DUSK", "mournful": "SORROW/DUSK",
    "weary": "SORROW/DUSK", "dull": "SORROW/DUSK", "dim": "SORROW/DUSK",
    "wistful": "SORROW/DUSK", "despair": "SORROW/DUSK", "dreary": "SORROW/DUSK",
    "affectionate": "LOVE/BLUSH", "caring": "LOVE/BLUSH", "romantic": "LOVE/BLUSH",
    "passion": "LOVE/BLUSH", "adore": "LOVE/BLUSH", "cherish": "LOVE/BLUSH",
    "sweet": "LOVE/BLUSH", "kiss": "LOVE/BLUSH", "cuddle": "LOVE/BLUSH",
    "blush": "LOVE/BLUSH", "flirt": "LOVE/BLUSH",
    "intimacy": "LOVE/BLUSH", "longing": "LOVE/BLUSH", "compassion": "LOVE/BLUSH",
    "devotion": "LOVE/BLUSH", "enamored": "LOVE/BLUSH", "fierce": "POWER/ANGER",
    "angry": "POWER/ANGER", "rage": "POWER/ANGER", "aggressive": "POWER/ANGER",
    "dominant": "POWER/ANGER", "bold": "POWER/ANGER", "brave": "POWER/ANGER",
    "fearless": "POWER/ANGER", "intense": "POWER/ANGER", "force": "POWER/ANGER",
    "storm": "POWER/ANGER", "flame": "POWER/ANGER", "determined": "POWER/ANGER",
    "assertive": "POWER/ANGER", "mighty": "POWER/ANGER", "warrior": "POWER/ANGER",
    "surge": "POWER/ANGER", "command": "POWER/ANGER", "calm": "PEACE/SERENITY",
    "serene": "PEACE/SERENITY", "tranquil": "PEACE/SERENITY", "quiet": "PEACE/SERENITY",
    "still": "PEACE/SERENITY", "relaxed": "PEACE/SERENITY", "ease": "PEACE/SERENITY",
    "mellow": "PEACE/SERENITY", "harmony": "PEACE/SERENITY", "gentle": "PEACE/SERENITY",
    "soothing": "PEACE/SERENITY", "balanced": "PEACE/SERENITY", "meditative": "PEACE/SERENITY",
    "composed": "PEACE/SERENITY", "breath": "PEACE/SERENITY", "zen": "PEACE/SERENITY",
    "warmth": "PEACE/SERENITY", "cozy": "PEACE/SERENITY", "comfort": "PEACE/SERENITY",
    "surprised": "SURPRISE/WONDER", "amazed": "SURPRISE/WONDER", "awe": "SURPRISE/WONDER",
    "party": "SURPRISE/WONDER", "unexpected": "SURPRISE/WONDER", "gasp": "SURPRISE/WONDER",
    "spark": "SURPRISE/WONDER", "shock": "SURPRISE/WONDER", "fascinated": "SURPRISE/WONDER",
    "magical": "SURPRISE/WONDER", "confetti": "SURPRISE/WONDER", "pop": "SURPRISE/WONDER",
    "disco": "SURPRISE/WONDER", "curious": "SURPRISE/WONDER", "dazzle": "SURPRISE/WONDER",
    "sparkle": "SURPRISE/WONDER", "neutral": "NEUTRAL/CLARITY", "steady": "NEUTRAL/CLARITY",
    "objective": "NEUTRAL/CLARITY", "clarity": "NEUTRAL/CLARITY", "moderate": "NEUTRAL/CLARITY",
    "simplicity": "NEUTRAL/CLARITY", "consistent": "NEUTRAL/CLARITY", "plain": "NEUTRAL/CLARITY",
    "simple": "NEUTRAL/CLARITY", "straightforward": "NEUTRAL/CLARITY", "transparent": "NEUTRAL/CLARITY",
    "average": "NEUTRAL/CLARITY", "centered": "NEUTRAL/CLARITY", "routine": "NEUTRAL/CLARITY",
    "standard": "NEUTRAL/CLARITY", "trust": "TRUST/SECURITY", "safe": "TRUST/SECURITY",
    "secure": "TRUST/SECURITY", "reliable": "TRUST/SECURITY", "credible": "TRUST/SECURITY",
    "confidence": "TRUST/SECURITY", "integrity": "TRUST/SECURITY", "honest": "TRUST/SECURITY",
    "dependable": "TRUST/SECURITY", "authentic": "TRUST/SECURITY", "guarantee": "TRUST/SECURITY",
    "stronghold": "TRUST/SECURITY", "encrypted": "TRUST/SECURITY", "verified": "TRUST/SECURITY",
    "support": "TRUST/SECURITY", "shield": "TRUST/SECURITY", "fear": "FEAR/ANXIETY",
    "scared": "FEAR/ANXIETY", "anxious": "FEAR/ANXIETY", "worry": "FEAR/ANXIETY",
    "panic": "FEAR/ANXIETY", "dread": "FEAR/ANXIETY", "nervous": "FEAR/ANXIETY",
    "terrified": "FEAR/ANXIETY", "alarm": "FEAR/ANXIETY", "threat": "FEAR/ANXIETY",
    "danger": "FEAR/ANXIETY", "uneasy": "FEAR/ANXIETY", "nightmare": "FEAR/ANXIETY",
    "stressful": "FEAR/ANXIETY", "tense": "FEAR/ANXIETY", "afraid": "FEAR/ANXIETY",
    "jittery": "FEAR/ANXIETY", "horror": "FEAR/ANXIETY", "doubt": "FEAR/ANXIETY"

}

ml_label_mapping = { "admiration": "JOY/HAPPINESS", "amusement": "JOY/HAPPINESS", "anger": "POWER/ANGER",
    "annoyance": "POWER/ANGER", "approval": "JOY/HAPPINESS", "caring": "LOVE/BLUSH",
    "confusion": "NEUTRAL/CLARITY", "curiosity": "SURPRISE/WONDER", "desire": "LOVE/BLUSH",
    "disappointment": "SORROW/DUSK", "disapproval": "POWER/ANGER", "disgust": "POWER/ANGER",
    "embarrassment": "SORROW/DUSK", "excitement": "JOY/HAPPINESS", "fear": "FEAR/ANXIETY",
    "gratitude": "LOVE/BLUSH", "grief": "SORROW/DUSK", "joy": "JOY/HAPPINESS",
    "love": "LOVE/BLUSH", "nervousness": "FEAR/ANXIETY", "optimism": "JOY/HAPPINESS",
    "pride": "JOY/HAPPINESS", "realization": "NEUTRAL/CLARITY", "relief": "JOY/HAPPINESS",
    "remorse": "SORROW/DUSK", "sadness": "SORROW/DUSK", "surprise": "SURPRISE/WONDER",
    "neutral": "NEUTRAL/CLARITY"
}

negation_words = {"not", "never", "no", "n't"}
opposite_emotions = {
    "JOY/HAPPINESS": "SORROW/DUSK",
    "SORROW/DUSK": "JOY/HAPPINESS",
    "LOVE/BLUSH": "NEUTRAL/CLARITY",
    "POWER/ANGER": "PEACE/SERENITY",
    "PEACE/SERENITY": "POWER/ANGER",
    "SURPRISE/WONDER": "NEUTRAL/CLARITY",
    "NEUTRAL/CLARITY": "NEUTRAL/CLARITY",
    "TRUST/SECURITY": "FEAR/ANXIETY",
    "FEAR/ANXIETY": "TRUST/SECURITY"
}

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    try:
        data = request.json
        if not data or 'text' not in data:
            logging.error("Missing 'text' field in JSON")
            return jsonify({"error": "Missing 'text' field in JSON"}), 400

        user_input = data['text'].lower().strip()
        if not user_input:
            logging.error("Empty text input")
            return jsonify({"error": "Empty text input"}), 400

        # 1️⃣ First: Keyword-based detection with negation
        detected_emotion = None
        doc = nlp(user_input)
        for token in doc:
            if token.text in emotion_mapping:
                has_negation = any(
                    neg in [t.text for t in doc[:token.i + 1]]
                    for neg in negation_words
                )
                if has_negation:
                    detected_emotion = opposite_emotions.get(
                        emotion_mapping[token.text], "NEUTRAL/CLARITY"
                    )
                else:
                    detected_emotion = emotion_mapping[token.text]
                break

        if detected_emotion:
            mapped_emotion = detected_emotion
            source = "Keyword Match"
        else:
            print("Before ML prediction")
            # 2️⃣ Fallback: ML prediction
            predicted_labels, dominant_label = predict_emotion(user_input, threshold=best_threshold)
            print(f"ML prediction done: {predicted_labels}, {dominant_label}")
            mapped_emotion = ml_label_mapping.get(dominant_label, "NEUTRAL/CLARITY")
            source = f"ML Label: {dominant_label}"

        print("Before parse_prompt")
        # 3️⃣ Now parse extra design hints
        parsed_data = parse_prompt(user_input)
        print("Before merge_prompt_with_spec")
        final_design = merge_prompt_with_spec(parsed_data, design_data, mapped_emotion)
        print("Before generate_moodboard")
        # 4️⃣ Generate moodboard
        output_path, session_log = generate_moodboard(parsed_data, mapped_emotion)
        print("After generate_moodboard")

        # Convert output_path to a URL for frontend access
        static_folder = os.path.join('static', 'moodboards')
        if static_folder in output_path:
            image_filename = output_path.split(static_folder)[-1].lstrip(os.sep)
            moodboard_url = url_for('static', filename=f"moodboards/{image_filename}")
        else:
            moodboard_url = output_path  # fallback: return path if not in static

        logging.info(
            f"Input: {user_input} | Source: {source} | "
            f"Mapped: {mapped_emotion} | Parsed: {parsed_data}"
        )

        return jsonify({
            "source": source,
            "mapped_category": mapped_emotion,
            "parsed_keywords": parsed_data,
            "design": final_design,
            "moodboard_path": output_path,
            "moodboard_url": moodboard_url
        })

    except Exception as e:
        import traceback
        logging.error(f"Server error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
