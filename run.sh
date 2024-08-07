#!/bin/bash

# Function to detect the operating system and set the appropriate python command and browser open command
detect_os() {
  if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PYTHON_CMD="python3"
    BROWSER_CMD="xdg-open"
  elif [[ "$OSTYPE" == "darwin"* ]]; then
    PYTHON_CMD="python3"
    BROWSER_CMD="open"
  elif [[ "$OSTYPE" == "cygwin" ]]; then
    PYTHON_CMD="python"
    BROWSER_CMD="cygstart"
  elif [[ "$OSTYPE" == "msys" ]]; then
    PYTHON_CMD="python"
    BROWSER_CMD="start"
  elif [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
    BROWSER_CMD="start"
  else
    echo "Unsupported OS type: $OSTYPE"
    exit 1
  fi
}

# Detect the OS and set the python and browser open commands
detect_os

# Start virtual environment
source env/bin/activate

# Create necessary directories
mkdir -p static/uploads

# Run the create_database.py script
$PYTHON_CMD utils/create_database.py

# Run the Flask application in the background
$PYTHON_CMD main.py &

# Wait for a few seconds to ensure the Flask server is up
sleep 2

# Open the default web browser to the Flask application's URL
$BROWSER_CMD "http://127.0.0.1:5000"
