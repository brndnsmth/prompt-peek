#!/bin/bash

echo "Checking Python version..."

# Get Python version
PYTHON_VERSION=$(python3 -V 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

# Check if Python is at least 3.10
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "Python 3.10 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python version is sufficient: $PYTHON_VERSION"

echo "Setting up the Flask environment..."

# Check if virtual environment exists, if not, create one
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the Flask app on port 5008
echo "Starting Flask app on port 5008..."
python app.py --port 5008
