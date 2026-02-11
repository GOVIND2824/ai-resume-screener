<<<<<<< HEAD
from pypdf import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
=======
from pypdf import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
>>>>>>> 19ea6d2c8a3837cd04c6a11358f9b8563a5695b5
