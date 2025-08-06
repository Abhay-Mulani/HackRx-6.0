def validate_file_type(filename):
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise ValueError("Only PDF and DOCX files are supported") 