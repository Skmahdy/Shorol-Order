from typing import Dict, List, Any
import time

from pipeline.cleaner import TextCleaner
from pipeline.batch_splitter import BatchSplitter
from pipeline.extractor import extractor
from pipeline.validator import validator
from pipeline.fixer import fixer
from pipeline.correction import corrector


class ProcessingResult:
    """Result of processing a text block with debug checkpoints."""

    def __init__(
        self,
        block: str,
        raw_output: Dict[str, Any],
        auto_fixed_output: Dict[str, Any],
        final_output: Dict[str, Any],
        retry_count: int = 0,
        errors: List[str] = None,
    ):
        self.block = block
        self.raw_output = raw_output
        self.auto_fixed_output = auto_fixed_output
        self.final_output = final_output
        self.retry_count = retry_count
        self.errors = errors or []
        self.needs_review = final_output.get("status") == "needs_review"


class TextProcessor:
    """Main processing orchestrator."""

    def __init__(self):
        self.cleaner = TextCleaner()
        self.splitter = BatchSplitter()

    def process_text(self, raw_text: str) -> Dict[str, Any]:
        """Process raw text through the full pipeline."""
        start_time = time.time()

        cleaned = self.cleaner.clean(raw_text)
        blocks = self.splitter.split(cleaned)

        all_results: List[ProcessingResult] = []
        total_retry_count = 0

        for block in blocks:
            result = self._process_block(block)
            all_results.append(result)
            total_retry_count += result.retry_count

        all_orders: List[Dict[str, Any]] = []
        all_errors: List[str] = []
        needs_review_count = 0

        debug_raw = []
        debug_auto_fix = []
        debug_final = []

        for index, result in enumerate(all_results):
            if result.final_output.get("orders"):
                all_orders.extend(result.final_output["orders"])
            if result.errors:
                all_errors.extend(result.errors)
            if result.needs_review:
                needs_review_count += 1

            debug_raw.append(
                {
                    "block_index": index,
                    "block_text": result.block,
                    "data": result.raw_output,
                }
            )
            debug_auto_fix.append(
                {
                    "block_index": index,
                    "block_text": result.block,
                    "data": result.auto_fixed_output,
                }
            )
            debug_final.append(
                {
                    "block_index": index,
                    "block_text": result.block,
                    "data": result.final_output,
                    "errors": result.errors,
                    "retry_count": result.retry_count,
                }
            )

        processing_time = time.time() - start_time

        return {
            "results": {"orders": all_orders},
            "processing_time": f"{processing_time:.2f}s",
            "processing_time_seconds": round(processing_time, 3),
            "retry_count": total_retry_count,
            "blocks_processed": len(blocks),
            "needs_review": needs_review_count > 0,
            "errors": all_errors if all_errors else [],
            "debug": {
                "raw_ai_extraction_output": debug_raw,
                "after_auto_fix": debug_auto_fix,
                "final_validated_result": debug_final,
            },
        }

    def _process_block(self, block: str) -> ProcessingResult:
        """Process a single text block."""
        retry_count = 0

        raw_output = extractor.extract(block)
        validated = validator.validate(raw_output)

        if validated.is_valid:
            return ProcessingResult(
                block=block,
                raw_output=raw_output,
                auto_fixed_output=raw_output,
                final_output=raw_output,
                retry_count=0,
                errors=[],
            )

        auto_fixed_output = fixer.auto_fix(raw_output)
        revalidated = validator.validate(auto_fixed_output)

        if revalidated.is_valid:
            return ProcessingResult(
                block=block,
                raw_output=raw_output,
                auto_fixed_output=auto_fixed_output,
                final_output=auto_fixed_output,
                retry_count=0,
                errors=[],
            )

        corrected = corrector.retry(block, revalidated, retry_count)
        retry_count += 1
        final_validated = validator.validate(corrected)

        if not final_validated.is_valid and retry_count < 2:
            corrected = corrector.retry(block, final_validated, retry_count)
            retry_count += 1
            final_validated = validator.validate(corrected)

        return ProcessingResult(
            block=block,
            raw_output=raw_output,
            auto_fixed_output=auto_fixed_output,
            final_output=corrected,
            retry_count=retry_count,
            errors=final_validated.errors,
        )


processor = TextProcessor()
