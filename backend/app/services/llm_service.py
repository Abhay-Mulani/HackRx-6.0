import os
import requests
import json

def query_llm(question: str, context: str = "") -> str:
    """Query LLM with document context"""
    
    # Try Groq first (free tier available)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        return query_groq(question, context, groq_api_key)
    
    # Fallback to Grok
    grok_api_key = os.getenv("GROK_API_KEY")
    if grok_api_key:
        return query_grok(question, context, grok_api_key)
    
    # If no API keys, return intelligent fallback
    return generate_fallback_response(question, context)

def query_groq(question: str, context: str, api_key: str) -> str:
    """Query Groq API (free tier available)"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Truncate context to avoid token limits
    if len(context) > 2000:
        context = context[:2000] + "... [truncated]"
    
    payload = {
        "messages": [
            {
                "role": "system", 
                "content": "You are a helpful document analysis assistant. Answer questions based on the provided document context. Be concise but informative."
            },
            {
                "role": "user", 
                "content": f"Document Context:\n{context}\n\nQuestion: {question}\n\nPlease provide a clear answer based on the document content."
            }
        ],
        "model": "llama3-8b-8192",  # Free tier model
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Groq API temporarily unavailable: {e}. Using document analysis fallback."

def query_grok(question: str, context: str, api_key: str) -> str:
    """Query Grok API (fallback)"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {"role": "system", "content": "You are a document analysis assistant."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0.2,
        "max_tokens": 400
    }
    
    try:
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Grok API error: {e}"

def generate_fallback_response(question: str, context: str) -> str:
    """Generate an intelligent response without external APIs"""
    if not context:
        return "No document content available to analyze. Please upload a document first."
    
    # Simple keyword-based analysis
    question_lower = question.lower()
    context_lower = context.lower()
    
    # Look for specific question types
    if any(word in question_lower for word in ['what is', 'what are', 'define', 'explain']):
        # Find sentences containing key terms from the question
        question_words = [w for w in question.split() if len(w) > 3]
        relevant_sentences = []
        
        for sentence in context.split('.'):
            if any(word.lower() in sentence.lower() for word in question_words):
                relevant_sentences.append(sentence.strip())
                if len(relevant_sentences) >= 2:
                    break
        
        if relevant_sentences:
            return f"Based on the document: {'. '.join(relevant_sentences)}."
    
    elif any(word in question_lower for word in ['how', 'when', 'where', 'why']):
        # Look for procedural or factual information
        sentences = [s.strip() for s in context.split('.') if s.strip()]
        if len(sentences) >= 3:
            return f"According to the document: {'. '.join(sentences[:3])}."
    
    # Default: return document summary
    sentences = context.split('.')[:3]
    summary = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
    return f"Document summary: {summary}\n\nFor specific questions, please provide an API key for enhanced AI analysis."