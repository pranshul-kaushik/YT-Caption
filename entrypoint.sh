#!/bin/bash

# Start the Flask health check server in the background
python3 src/apis/health_check.py &

# Start the Streamlit app
python3 -m streamlit run src/main.py