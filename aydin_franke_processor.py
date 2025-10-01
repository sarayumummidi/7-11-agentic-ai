import fitz  # This is PyMuPDF that Sai recommended
import pytesseract # Have to install tesseract separately and add to PATH
from PIL import Image
import io
import json
from pathlib import Path


class FrankePDFProcessor:
    """Process Franke Coffee Systems PDFs for RAG system"""

    def __init__(self, tesseract_path: str = None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def extract_text_and_metadata(self, pdf_path: str):
        """Extract text, images, and metadata from PDF"""
        doc = fitz.open(pdf_path)

        result = {
            'file_name': Path(pdf_path).name,
            'total_pages': len(doc),
            'text_content': [],
            'tables': [],
            'images': [],
            'metadata': doc.metadata
        }

        for page_num in range(len(doc)):
            page = doc[page_num]

            text = page.get_text()

            # If the text is really short (less than 50 chars), the page wont have selectable text
            # In this case it uses OCR to extract text from the image of the page
            if len(text.strip()) < 50:
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                ocr_text = pytesseract.image_to_string(img)
                text = ocr_text if len(ocr_text) > len(text) else text

            result['text_content'].append({
                'page': page_num + 1,
                'text': text,
                'char_count': len(text)
            })

            # Extract the images
            image_list = page.get_images()
            for img_index, img in enumerate(image_list):
                result['images'].append({
                    'page': page_num + 1,
                    'image_index': img_index,
                    'xref': img[0]
                })

        doc.close()
        return result

    def chunk_text(self, text: str, chunk_size: int = 400, overlap: int = 50):
        """Split text into chunks for embedding (300 to 500 tokens)"""
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())

        return chunks

    def process_franke_pdf(self, pdf_path: str):
        """Main processing function for Franke PDFs"""
        print(f"Processing: {pdf_path}")

        content = self.extract_text_and_metadata(pdf_path) # Extract content
        full_text = '\n'.join([page['text'] for page in content['text_content']]) # Combine all text
        chunks = self.chunk_text(full_text) # Create chunks

        # Add chunked content to result
        content['chunks'] = chunks
        content['chunk_count'] = len(chunks)

        print(f"Processed {content['total_pages']} pages and created {len(chunks)} chunks")

        return content


# Test usage (change later to run in pipeline)
processor = FrankePDFProcessor()

pdf_path = "data/raw_pdfs/20109399_User manual_A1000_en 1.pdf"  # Change path to test it
result = processor.process_franke_pdf(pdf_path)

output_path = "data/processed/A1000_processed.json" # Might have to create folders first if they don't exist
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"Done")
