#!/bin/bash

echo "🛡️  EDR Dashboard Startup Script"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment. Please install python3-venv:"
        echo "   sudo apt install python3-venv python3-full"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi

# Create necessary directories
mkdir -p static/css static/js

# Start the EDR dashboard
echo "🚀 Starting EDR Dashboard..."
echo "   Dashboard will be available at: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo ""

python app.py