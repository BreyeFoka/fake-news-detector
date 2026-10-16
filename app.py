from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import re
import string
import os
from datetime import datetime

MODEL_NAME = "facebook/bart-large-mnli"
_classifier = None


def get_classifier():
    """Load the zero-shot model on first use, so importing the app (and testing it) stays light."""
    global _classifier
    if _classifier is None:
        from transformers import pipeline

        _classifier = pipeline("zero-shot-classification", model=MODEL_NAME)
    return _classifier

# Flask setup
app = Flask(__name__)

# CORS configuration - get allowed origins from environment variable
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
print("Allowed origins:", allowed_origins)

CORS(app, origins=allowed_origins, methods=["GET", "POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Text cleaning function
def clean_text(text):
    """Clean and preprocess text for better model performance"""
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r"\d+", "", text)  # Remove numbers
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace
    return text

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME
    })

# Check if server is running fine
@app.route("/healthCheck", methods=["POST"])
def checkHealth():
    return jsonify({"success": "Server Up and Running"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    """Main prediction endpoint"""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        headline = data.get("headline", "")
        content = data.get("text", "")
        
        if not headline and not content:
            return jsonify({"error": "Please provide either headline or text"}), 400
        
        # Combine and clean text
        full_text = clean_text(f"{headline} {content}")
        
        if len(full_text.strip()) < 5:
            return jsonify({"error": "Text too short for meaningful analysis"}), 400
        
        # Zero-shot classification
        result = get_classifier()(full_text, candidate_labels=["Real", "Fake"])
        
        prediction = result["labels"][0].lower()  # top label
        confidence = round(result["scores"][0] * 100, 2)  # top score as percentage
        
        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "analysis": {
                "text_length": len(full_text),
                "headline": headline[:100] + "..." if len(headline) > 100 else headline,
                "content_preview": content[:100] + "..." if len(content) > 100 else content
            }
        })
        
    except Exception:
        logging.exception("Prediction failed")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
