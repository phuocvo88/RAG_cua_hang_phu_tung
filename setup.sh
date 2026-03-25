#!/bin/bash
# Setup script for Linux/Mac - equivalent to install_python.ps1

set -e  # Exit on any error

echo "Setting up Python environment for RAG application..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.11 or higher first."
    echo ""
    echo "Installation instructions:"
    echo "  Ubuntu/Debian: sudo apt-get update && sudo apt-get install python3.11"
    echo "  macOS: brew install python@3.11"
    echo "  Fedora: sudo dnf install python3.11"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Warning: Python $PYTHON_VERSION is installed, but $REQUIRED_VERSION or higher is recommended."
fi

echo "Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install backend dependencies
if [ -f "backend/requirements.txt" ]; then
    echo "Installing backend dependencies from requirements.txt..."
    pip install -r backend/requirements.txt
    echo "Backend dependencies installed successfully."
else
    echo "Warning: backend/requirements.txt not found."
fi

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ] && [ -f "backend/.env.example" ]; then
    echo "Creating .env file from .env.example..."
    cp backend/.env.example backend/.env
    echo ".env file created. Please edit backend/.env and add your API keys."
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env and add your API keys (GOOGLE_API_KEY, ANTHROPIC_API_KEY)"
echo "  2. Make sure Gradle wrapper is executable: chmod +x gradlew"
echo "  3. Run the application: ./gradlew runAll"
echo ""
echo "To activate the virtual environment later, run:"
echo "  source venv/bin/activate"
