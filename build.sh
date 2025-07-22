#!/bin/bash
# Render build script

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo "Creating static directories..."
mkdir -p backend/static/moodboards

echo "Build complete!"
