import gc
from typing import List

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    """
    Memory-efficient text chunking for Render free tier
    """
    try:
        # Handle empty or small text
        if not text or len(text) < chunk_size:
            return [text] if text else [""]
        
        chunks = []
        start = 0
        
        # Limit total chunks to prevent memory issues
        max_chunks = 20  # Reasonable limit for free tier
        chunk_count = 0
        
        while start < len(text) and chunk_count < max_chunks:
            end = start + chunk_size
            
            # Try to break at word boundary
            if end < len(text):
                # Find the last space within the chunk
                space_idx = text.rfind(' ', start, end)
                if space_idx > start:
                    end = space_idx
            
            chunk = text[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)
                chunk_count += 1
            
            start = end - overlap if end < len(text) else end
        
        # Force garbage collection
        gc.collect()
        
        return chunks
        
    except Exception as e:
        # Return simple chunks on error
        return [text[:300]] if text else [""] 