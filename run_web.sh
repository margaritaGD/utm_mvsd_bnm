#!/bin/bash

export PYTHONPATH=${PYTHONPATH}:$(pwd)
cd src/main/web
streamlit run chatbot.py