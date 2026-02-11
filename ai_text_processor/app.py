from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from pipeline.processor import processor

# Create FastAPI app
app = FastAPI(
    title="Shorol-Order AI Text Processor",
    description="Text-only AI pipeline for order extraction",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProcessTextRequest(BaseModel):
    """Request model for text processing."""
    text: str


class ProcessTextResponse(BaseModel):
    """Response model for text processing."""
    results: dict
    processing_time: str
    retry_count: int
    blocks_processed: int
    needs_review: bool
    errors: list = None


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the UI."""
    ui_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    try:
        with open(ui_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <head><title>Shorol-Order AI Text Processor</title></head>
            <body>
                <h1>Shorol-Order AI Text Processor</h1>
                <p>UI file not found. Please create ui/index.html</p>
                <p>API endpoint: POST /process-text</p>
            </body>
        </html>
        """


@app.post("/process-text", response_model=ProcessTextResponse)
async def process_text(request: ProcessTextRequest):
    """
    Process raw text through AI extraction pipeline.
    
    Args:
        request: ProcessTextRequest with raw text
        
    Returns:
        ProcessTextResponse with structured results
    """
    try:
        result = processor.process_text(request.text)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "results": {"orders": []},
                "processing_time": "0s",
                "retry_count": 0,
                "blocks_processed": 0,
                "needs_review": True,
                "errors": [str(e)]
            }
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "ai-text-processor"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
