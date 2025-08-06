# HackRx 6.0 - Intelligent Document Query Retrieval System

An intelligent document query retrieval system built for HackRx 6.0 hackathon. This system allows users to upload documents and query them using natural language processing.

## 🚀 Features

- **Document Upload**: Support for PDF and DOCX files
- **Intelligent Query Processing**: Natural language queries on uploaded documents
- **Vector Search**: Advanced vector-based document search using embeddings
- **Real-time Results**: Fast query processing and response
- **Modern UI**: Clean and intuitive user interface
- **RESTful API**: FastAPI-based backend with comprehensive endpoints

## 🏗️ Architecture

### Backend
- **FastAPI**: Modern Python web framework
- **Vector Database**: Pinecone for vector storage and similarity search
- **LLM Integration**: Support for multiple LLM providers (Gemini, Grok)
- **Document Processing**: PDF and DOCX parsing with intelligent chunking
- **Authentication**: JWT-based API security

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Modern CSS**: Responsive design with animations
- **Axios**: HTTP client for API communication
- **Component-based**: Modular Vue components

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd "Bajaj Hackrx"
```

### 2. Backend Setup
```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt
```

### 3. Frontend Setup
```bash
# Install dependencies
npm install
```

### 4. Environment Configuration
Create a `.env` file in the root directory:
```env
# API Configuration
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_for_jwt_here

# LLM Configuration (Choose one)
GEMINI_API_KEY=your_gemini_api_key_here
GROK_API_KEY=your_grok_api_key_here

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/hackrx_db

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here

# Application Settings
DEBUG=true
```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend Server
```bash
python -m http.server 3000 --directory frontend
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints.py
│   │   │   │   └── schemas.py
│   │   │   ├── documents.py
│   │   │   ├── hackrx.py
│   │   │   └── queries.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── embeddings.py
│   │   │   └── security.py
│   │   ├── models/
│   │   │   └── document.py
│   │   ├── services/
│   │   │   ├── document_processor.py
│   │   │   ├── llm_service.py
│   │   │   ├── parser.py
│   │   │   └── vector_db.py
│   │   ├── utils/
│   │   │   ├── chunking.py
│   │   │   ├── document_parser.py
│   │   │   └── validation.py
│   │   └── main.py
│   └── venv/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DocumentUpload.vue
│   │   │   ├── Leaderboard.vue
│   │   │   └── QueryInput.vue
│   │   ├── animations.js
│   │   ├── app.js
│   │   └── style.css
│   └── index.html
├── package.json
├── requirements.txt
└── README.md
```

## 🔧 API Endpoints

### Document Management
- `POST /hackrx/upload` - Upload document
- `POST /hackrx/run` - Query document

### Authentication
- API key required for all endpoints
- JWT token support for user authentication

## 🧪 Testing

The API documentation is available at `http://localhost:8000/docs` when the backend server is running.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 HackRx 6.0

This project was developed for the HackRx 6.0 hackathon, focusing on intelligent document processing and query retrieval systems.

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Pinecone Documentation](https://docs.pinecone.io/)

---

Made with ❤️ for HackRx 6.0
