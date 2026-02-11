# AI Text Processor

Standalone Python app for extracting structured order data from messy Bangladeshi chat text.

## Features

- Clean and normalize Bangladeshi text (Bengali digits, emojis, etc.)
- Split text by phone numbers or line breaks
- AI-based extraction using OpenAI
- Strict JSON validation
- Auto-fix common issues
- Correction loop with retries
- Temporary debug UI

## Setup

1. Install dependencies:
```bash
cd ai_text_processor
pip install -r requirements.txt
```

2. Set OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

3. Run the server:
```bash
python app.py
```

4. Open browser:
```
http://localhost:8000
```

## Project Structure

```
ai_text_processor/
├── app.py                # FastAPI entry
├── config.py             # API keys + model settings
├── pipeline/
│   ├── cleaner.py        # Text cleaning
│   ├── batch_splitter.py # Split by phone numbers
│   ├── extractor.py      # AI extraction
│   ├── validator.py      # JSON validation
│   ├── fixer.py          # Auto-fix issues
│   ├── correction.py     # Retry logic
│   └── processor.py      # Main orchestrator
├── prompts/
│   ├── system_prompt.txt
│   └── correction_prompt.txt
├── ui/
│   └── index.html        # Temporary UI
└── test_samples/
    └── messy_samples.txt
```

## API

### POST /process-text

Request:
```json
{
  "text": "raw messy input"
}
```

Response:
```json
{
  "results": {
    "orders": [...]
  },
  "processing_time": "0.45s",
  "retry_count": 0,
  "blocks_processed": 1,
  "needs_review": false,
  "errors": null
}
```

## JSON Schema

All output follows this schema:

```json
{
  "orders": [
    {
      "customer_name": "string | null",
      "phone": "string | null",
      "address": "string | null",
      "item": "string | null",
      "quantity": "integer | null",
      "notes": "string | null"
    }
  ]
}
```

## Testing

Test with samples in `test_samples/messy_samples.txt`:

1. Single clean order
2. Messy Banglish
3. Bengali digits
4. Two phone numbers
5. Missing phone
6. Quantity words like "duita"
7. With +88 prefix
8. Phone without leading 0
9. Multiple items
10. Very messy text

## Notes

- No database
- No courier integration
- No authentication
- Only extraction engine
- Modular architecture for easy expansion
