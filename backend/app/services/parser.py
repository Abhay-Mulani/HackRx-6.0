import PyPDF2
import zipfile
import xml.etree.ElementTree as ET
from fastapi import UploadFile
import io

async def parse_document(file: UploadFile) -> str:
    content = await file.read()
    
    if file.filename.endswith(".pdf"):
        pdf_file = io.BytesIO(content)
        reader = PyPDF2.PdfReader(pdf_file)
        return "".join(page.extract_text() for page in reader.pages)
    
    elif file.filename.endswith(".docx"):
        # Parse DOCX manually to avoid conflicts
        return parse_docx_content(content)
    
    else:
        raise ValueError("Unsupported file type")

def parse_docx_content(content: bytes) -> str:
    """Parse DOCX content manually without using python-docx to avoid conflicts"""
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as zip_file:
            # Read the main document
            doc_xml = zip_file.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            
            # Extract text from all text nodes
            text_content = []
            for elem in root.iter():
                if elem.text:
                    text_content.append(elem.text)
            
            return "\n".join(text_content)
    except Exception as e:
        raise ValueError(f"Error parsing DOCX file: {e}") 