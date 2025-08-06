
from app.core.config import settings
import pinecone

from sentence_transformers import SentenceTransformer

_index = None
# Use a 1024-dim model compatible with Pinecone index
_model = SentenceTransformer('BAAI/bge-large-en-v1.5')

def get_pinecone_index():
    global _index
    if _index is None:
        from pinecone import Pinecone
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        _index = pc.Index(
            settings.PINECONE_INDEX,
            host="https://hackrx-documents-nebxkgj.svc.aped-4627-b74a.pinecone.io"
        )
    return _index

def store_embeddings(chunks, document_id=1):
    index = get_pinecone_index()
    embeddings = _model.encode(chunks).tolist()
    vectors = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": f"doc-{document_id}-chunk-{i}",
            "values": emb,
            "metadata": {"text": chunk, "document_id": document_id}
        })
    index.upsert(vectors)

def search_similar_chunks(document_id, question):
    index = get_pinecone_index()
    
    # Create multiple search queries to find relevant information
    search_queries = [
        question,  # Original question
        "grace period premium payment thirty days",  # Specific terms
        "premium due date grace period days",  # Alternative phrasing
        "renewal premium payment grace"  # Another variation
    ]
    
    all_chunks = []
    chunk_texts = set()  # To avoid duplicates
    
    for query in search_queries:
        embedding = _model.encode([query])[0].tolist()
        # First try with document_id filter
        results = index.query(
            vector=embedding,
            top_k=3,
            include_metadata=True,
            filter={"document_id": document_id}
        )
        
        # If no results with filter, try without filter
        if not results['matches']:
            results = index.query(
                vector=embedding,
                top_k=3,
                include_metadata=True
            )
        
        # Collect unique chunks
        for match in results['matches']:
            text = match['metadata'].get('text', '')
            if text and text not in chunk_texts:
                chunk_texts.add(text)
                all_chunks.append(text)
    
    # Return up to 6 most relevant unique chunks
    return all_chunks[:6]