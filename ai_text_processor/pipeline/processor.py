from typing import Dict, List, Any
import time

from pipeline.cleaner import TextCleaner
from pipeline.batch_splitter import BatchSplitter
from pipeline.extractor import extractor
from pipeline.validator import validator
from pipeline.fixer import fixer
from pipeline.correction import corrector


class ProcessingResult:
    """Result of processing a text block."""
    
    def __init__(self, data: Dict[str, Any], retry_count: int = 0, errors: List[str] = None):
        self.data = data
        self.retry_count = retry_count
        self.errors = errors or []
        self.needs_review = data.get('status') == 'needs_review'


class TextProcessor:
    """
    Main processing orchestrator.
    
    Flow:
    1. Clean text
    2. Split into blocks
    3. For each block:
       - Extract with AI
       - Validate
       - Auto-fix if needed
       - Retry with correction if still invalid
    4. Aggregate results
    """
    
    def __init__(self):
        self.cleaner = TextCleaner()
        self.splitter = BatchSplitter()
    
    def process_text(self, raw_text: str) -> Dict[str, Any]:
        """
        Process raw text through the full pipeline.
        
        Args:
            raw_text: Raw messy input text
            
        Returns:
            Processing results with aggregated data
        """
        start_time = time.time()
        
        # Step 1: Clean
        cleaned = self.cleaner.clean(raw_text)
        
        # Step 2: Split into blocks
        blocks = self.splitter.split(cleaned)
        
        # Step 3: Process each block
        all_results = []
        total_retry_count = 0
        
        for block in blocks:
            result = self._process_block(block)
            all_results.append(result)
            total_retry_count += result.retry_count
        
        # Step 4: Aggregate results
        all_orders = []
        all_errors = []
        needs_review_count = 0
        
        for result in all_results:
            if result.data.get('orders'):
                all_orders.extend(result.data['orders'])
            if result.errors:
                all_errors.extend(result.errors)
            if result.needs_review:
                needs_review_count += 1
        
        processing_time = time.time() - start_time
        
        return {
            "results": {
                "orders": all_orders
            },
            "processing_time": f"{processing_time:.2f}s",
            "retry_count": total_retry_count,
            "blocks_processed": len(blocks),
            "needs_review": needs_review_count > 0,
            "errors": all_errors if all_errors else None
        }
    
    def _process_block(self, block: str) -> ProcessingResult:
        """
        Process a single text block.
        
        Args:
            block: Text block to process
            
        Returns:
            ProcessingResult
        """
        retry_count = 0
        
        # Initial extraction
        ai_output = extractor.extract(block)
        validated = validator.validate(ai_output)
        
        if not validated.is_valid:
            # Try auto-fix
            fixed = fixer.auto_fix(ai_output)
            revalidated = validator.validate(fixed)
            
            if not revalidated.is_valid:
                # Retry with correction
                corrected = corrector.retry(block, revalidated, retry_count)
                retry_count += 1
                final_validated = validator.validate(corrected)
                
                if not final_validated.is_valid and retry_count < 2:
                    # One more retry
                    corrected = corrector.retry(block, final_validated, retry_count)
                    retry_count += 1
                    final_validated = validator.validate(corrected)
                
                return ProcessingResult(corrected, retry_count, final_validated.errors)
            else:
                return ProcessingResult(fixed, 0, [])
        else:
            return ProcessingResult(ai_output, 0, [])


# Singleton instance
processor = TextProcessor()
