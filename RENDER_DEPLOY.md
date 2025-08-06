# Render Deployment Instructions

## Backend Deployment (render.yaml)
The render.yaml file will deploy the FastAPI backend automatically.

## Frontend Deployment (Manual)
After the backend is deployed, manually create a Static Site service:

1. In Render Dashboard, click "New +"
2. Select "Static Site"
3. Connect the same repository: Abhay-Mulani/HackRx-6.0
4. Set:
   - Build Command: `echo "No build needed"`
   - Publish Directory: `frontend`
5. Deploy

## Environment Variables for Backend
Set these in the backend service:
- API_KEY=hackrx_secure_api_key_2024
- SECRET_KEY=jwt_secret_key_for_hackrx_very_secure
- DEBUG=false
- GEMINI_API_KEY=your_gemini_api_key
- PINECONE_API_KEY=your_pinecone_api_key
- PINECONE_ENVIRONMENT=gcp-starter
