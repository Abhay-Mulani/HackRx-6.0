#!/usr/bin/env python3
"""
Test script for HackRx API compliance
Tests the exact format specified in the guidelines
"""

import requests
import json

# API endpoint
API_URL = "https://hackrx-backend-pw4u.onrender.com/hackrx/run"
API_KEY = "hackrx_secure_api_key_2024"

# Test data matching HackRx guidelines format
test_payload = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) treatment?",
        "Does this policy cover maternity expenses, and what are the waiting periods?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}

def test_api():
    """Test the API with HackRx format"""
    print("🚀 Testing HackRx API Compliance")
    print(f"📡 Endpoint: {API_URL}")
    print(f"🔑 Using API Key: {API_KEY}")
    print("\n📝 Request Format:")
    print(json.dumps(test_payload, indent=2))
    
    try:
        # Make the API call
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        print("\n⏳ Sending request...")
        response = requests.post(API_URL, json=test_payload, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"⏰ Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Response Format:")
            print(json.dumps(result, indent=2))
            
            # Validate response format
            if "answers" in result and isinstance(result["answers"], list):
                print(f"\n🎉 SUCCESS: API returns proper format!")
                print(f"📊 Questions processed: {len(test_payload['questions'])}")
                print(f"📊 Answers received: {len(result['answers'])}")
                
                if len(result['answers']) == len(test_payload['questions']):
                    print("✅ Answer count matches question count")
                else:
                    print("⚠️  Answer count doesn't match question count")
            else:
                print("❌ FAIL: Response doesn't match expected format")
                print("Expected: {'answers': [...]}")
        else:
            print(f"❌ FAIL: HTTP {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_api()
