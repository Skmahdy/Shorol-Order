# Shorol-Order

AI-powered order extraction system for Bangladesh F-commerce.

## Session 1: Text AI Processing

The `ai_text_processor` directory contains a standalone Python application that extracts structured order data from messy Bangladeshi chat text.

### Features

- ✅ Text cleaning and normalization (Bengali digits, emojis, etc.)
- ✅ Intelligent text splitting by phone numbers
- ✅ AI-based order extraction with OpenAI
- ✅ Strict JSON validation
- ✅ Auto-fix common issues
- ✅ Correction loop with retry logic
- ✅ Temporary debug UI

### Quick Start

```bash
cd ai_text_processor
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
python app.py
```

Then open http://localhost:8000 in your browser.

### Documentation

See [ai_text_processor/README.md](ai_text_processor/README.md) for detailed documentation.

## Project Structure

```
Shorol-Order/
└── ai_text_processor/          # Session 1: Text AI Processing
    ├── app.py                  # FastAPI application
    ├── config.py               # Configuration
    ├── pipeline/               # Processing modules
    │   ├── cleaner.py
    │   ├── batch_splitter.py
    │   ├── extractor.py
    │   ├── validator.py
    │   ├── fixer.py
    │   ├── correction.py
    │   └── processor.py
    ├── prompts/                # AI prompts
    ├── ui/                     # Temporary UI
    └── test_samples/           # Test cases
```