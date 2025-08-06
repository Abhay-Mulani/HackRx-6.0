from app.core.config import settings
import requests
import json
import time

def ask_llm(question, context_chunks):
    # Use Google Gemini Pro API for text generation
    api_key = settings.GEMINI_API_KEY
    context = "\n".join(context_chunks)
    # Use the new Gemini 1.5 Flash endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    # Build Gemini-style payload with enhanced prompt for better formatting
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"""Based on the following context from the policy document, provide a clear and comprehensive answer to the question. 

Context: {context}

Question: {question}

Please provide your answer in a well-structured format with:
1. A direct answer to the question
2. Supporting details from the context if available
3. Any relevant additional information

Answer:"""}
                ]
            }
        ]
    }
    import logging
    logging.info(f"Gemini request URL: {url}")
    logging.info(f"Gemini request payload: {json.dumps(payload)}")
    
    # Try with retry logic for service unavailable errors
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            logging.info(f"Gemini response: {response.status_code} {response.text}")
            
            if response.status_code == 503:
                if attempt < max_retries - 1:
                    logging.warning(f"Gemini service unavailable, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # Fallback response for service unavailable
                    return generate_fallback_response(question, context)
            
            response.raise_for_status()
            result = response.json()
            
            # Check if we have a valid response
            if 'candidates' in result and len(result['candidates']) > 0:
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()
            else:
                logging.error(f"Invalid Gemini response structure: {result}")
                return generate_fallback_response(question, context)
                
        except requests.exceptions.Timeout as e:
            logging.error(f"Gemini API timeout: {e}")
            if attempt < max_retries - 1:
                logging.warning(f"Retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                continue
            return generate_fallback_response(question, context)
        except Exception as e:
            logging.error(f"Gemini error: {e}, response: {getattr(e, 'response', None)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return generate_fallback_response(question, context)
    
    return generate_fallback_response(question, context)

def generate_fallback_response(question, context):
    """Generate a basic response when Gemini is unavailable"""
    # Simple keyword-based fallback
    question_lower = question.lower()
    context_lower = context.lower()
    
    # Look for specific keywords in the question and try to find relevant info in context
    if "grace period" in question_lower and "premium" in question_lower:
        if "thirty days" in context_lower or "30 days" in context_lower:
            return "Based on the document context, the grace period for premium payment appears to be 30 days. (Note: Generated using fallback processing due to service unavailability)"
    
    if "waiting period" in question_lower:
        if "months" in context_lower:
            return "Based on the document context, there appears to be a waiting period mentioned in the policy terms. Please refer to the source document for specific details. (Note: Generated using fallback processing due to service unavailability)"
    
    # Generic fallback
    if context.strip():
        return f"I found relevant information in the document context, but I'm currently unable to process it fully due to service unavailability. Please refer to the source document sections provided for detailed information about: {question}"
    else:
        return f"I apologize, but I'm currently unable to process your question '{question}' due to service unavailability. Please try again later or refer to the original document."