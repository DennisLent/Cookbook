#!/bin/bash

# Create the database
python create_database.py

# Set the FLASK_APP environment variable
export FLASK_APP=main

# Run the Flask app
flask run