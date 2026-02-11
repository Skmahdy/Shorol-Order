#!/bin/bash
# Quick start script for AI Text Processor

echo "🚀 Starting Shorol-Order AI Text Processor"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Please run this script from the ai_text_processor directory"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
    echo "   The app will run in mock mode for testing"
    echo "   To use real AI extraction, set: export OPENAI_API_KEY='your-key'"
    echo ""
fi

# Run tests first
echo "🧪 Running tests..."
python3 test_pipeline.py
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi
echo ""

# Start the server
echo "✅ Tests passed!"
echo "🌐 Starting server on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""

python3 app.py
