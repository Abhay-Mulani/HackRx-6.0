import PyPDF2
from io import BytesIO
import zipfile
import xml.etree.ElementTree as ET
import logging

async def parse_document_from_bytes(content: bytes, filename: str) -> str:
    """Parse document from bytes content"""
    try:
        if filename.lower().endswith('.pdf'):
            return parse_pdf_from_bytes(content)
        elif filename.lower().endswith('.docx'):
            return parse_docx_from_bytes(content)
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    except Exception as e:
        logging.error(f"Error parsing document {filename}: {e}")
        raise

def parse_pdf_from_bytes(content: bytes) -> str:
    """Parse PDF from bytes"""
    pdf_file = BytesIO(content)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def parse_docx_from_bytes(content: bytes) -> str:
    """Parse DOCX from bytes using manual XML parsing"""
    try:
        docx_file = BytesIO(content)
        with zipfile.ZipFile(docx_file, 'r') as zip_file:
            # Read the main document XML
            xml_content = zip_file.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Extract text from XML
            text = ""
            for elem in root.iter():
                if elem.text:
                    text += elem.text + " "
            
            return text.strip()
    except Exception as e:
        logging.error(f"Error parsing DOCX: {e}")
        raise ValueError(f"Error parsing DOCX file: {e}")
