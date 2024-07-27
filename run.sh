#!/bin/bash

# Function to detect the operating system and set the appropriate python command
detect_os() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PYTHON_CMD="python3"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
  elif [[ "$OSTYPE" == "cygwin" ]]; then
    PYTHON_CMD="python"
  elif [[ "$OSTYPE" == "msys" ]]; then
    PYTHON_CMD="python"
  elif [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
  else
    echo "Unsupported OS type: $OSTYPE"
    exit 1
  fi
}

# Detect the OS and set the python command
detect_os

# Create necessary directories
mkdir -p static/uploads

# Run the create_database.py script
$PYTHON_CMD utils/create_database.py

# Run the Flask application
$PYTHON_CMD main.py
