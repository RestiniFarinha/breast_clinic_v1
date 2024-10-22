#!/bin/bash

cd /app/

echo "activating environment"
python -m venv .venv
source .venv/bin/activate

echo "installing dependencies"
pip install -r requirements.txt --quiet

echo "running streamlit application"
streamlit run streamlit_app.py
