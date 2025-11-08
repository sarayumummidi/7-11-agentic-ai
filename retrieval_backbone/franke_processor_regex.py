import fitz # This is PyMuPDF that Sai recommended
import pytesseract # Have to install tesseract separately and add to PATH
from PIL import Image
import io
import json
import re
from pathlib import Path
from VectorDB import VectorDB


class FrankePDFProcessor:
    """Process Franke Coffee Systems PDFs for RAG system"""

    def __init__(self, tesseract_path=None, target_tokens=400, overlap_tokens=50):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

        self.target_tokens = target_tokens
        self.overlap_tokens = overlap_tokens

    def extract_text_and_metadata(self, pdf_path):
        """Extract text, images, and metadata from PDF"""
        doc = fitz.open(pdf_path)

        result = {
            'file_name': Path(pdf_path).name,
            'total_pages': len(doc),
            'text_content': [],
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

    def clean_text(self, text):
        """Clean the text by removing headers, footers, excessive whitespace"""
        # Remove stuff that appear on every page (got what to get rid of from ChatGPT)
        text = re.sub(r'Franke Kaffeemaschinen AG', '', text, flags=re.IGNORECASE)
        text = re.sub(r'User manual A1000', '', text, flags=re.IGNORECASE)

        # Remove the \n and whitespace
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r' +', ' ', text)

        # Remove repeated page numbers
        text = re.sub(r'\b\d{1,3}\b\s*$', '', text)
        text = re.sub(r'^\s*\d{1,3}\b', '', text)

        return text.strip()

    def estimate_tokens(self, text):
        """Estimate of the count estimation"""
        return int(len(text.split()) * 0.75)

    def chunk_page(self, page_data, global_chunk_id):
        """Chunk a single page into 300 to 500 token segments"""
        text = self.clean_text(page_data['text'])
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self.estimate_tokens(sentence)

            # Save chunk if adding this sentence would exceed target
            if current_tokens + sentence_tokens > self.target_tokens and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'token_count': current_tokens,
                    'metadata': {
                        'source_page': page_data['page'],
                        'chunk_id': global_chunk_id
                    }
                })
                global_chunk_id += 1

                # Keep some overlap for context
                overlap_words = ' '.join(current_chunk).split()[-self.overlap_tokens:]
                current_chunk = [' '.join(overlap_words), sentence]
                current_tokens = self.estimate_tokens(' '.join(current_chunk))
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens

        # Add remaining text as final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'token_count': current_tokens,
                'metadata': {
                    'source_page': page_data['page'],
                    'chunk_id': global_chunk_id
                }
            })
            global_chunk_id += 1

        return chunks, global_chunk_id

    def chunk_document(self, doc_data):
        """Chunk entire document into 300-500 token segments"""
        all_chunks = []
        global_chunk_id = 0

        for page in doc_data['text_content']:
            page_chunks, global_chunk_id = self.chunk_page(page, global_chunk_id)
            all_chunks.extend(page_chunks)

        # Calculate stats
        if all_chunks:
            token_counts = [c['token_count'] for c in all_chunks]
            min_tokens = min(token_counts)
            max_tokens = max(token_counts)
            avg_tokens = sum(token_counts) / len(token_counts)
        else:
            min_tokens = max_tokens = avg_tokens = 0

        return {
            'file_name': doc_data['file_name'],
            'total_pages': doc_data['total_pages'],
            'total_chunks': len(all_chunks),
            'chunks': all_chunks,
            'chunk_stats': {
                'min_tokens': min_tokens,
                'max_tokens': max_tokens,
                'avg_tokens': avg_tokens
            }
        }

    def process_franke_pdf(self, pdf_path):
        """Main function to process PDF and create chunks"""
        print(f"Processing: {pdf_path}")

        # Extract text from the PDF
        content = self.extract_text_and_metadata(pdf_path)
        print(f"Extracted {content['total_pages']} pages")

        # Chunk the text
        chunked_data = self.chunk_document(content)
        print(f"Created {chunked_data['total_chunks']} chunks")

        # Print stuff
        stats = chunked_data['chunk_stats']
        print(f"Token range: {stats['min_tokens']}-{stats['max_tokens']}, avg: {stats['avg_tokens']:.1f}")

        return content, chunked_data


# Testing from pycharm
processor = FrankePDFProcessor(target_tokens=400, overlap_tokens=50)

pdf_path = r"C:\Users\Aydin\Projects\Python\BTT\7-11B\data\dataset.pdf" # Change path to test it
processed_result, chunked_result = processor.process_franke_pdf(pdf_path)

# Save both versions (thanks ChatGPT for this part)
output_dir = Path(r"C:\Users\Aydin\Projects\Python\BTT\7-11B\data")
output_dir.mkdir(parents=True, exist_ok=True)

processed_path = output_dir / "A1000_processed.json"
with open(processed_path, 'w', encoding='utf-8') as f:
    json.dump(processed_result, f, indent=2, ensure_ascii=False)

chunked_path = output_dir / "A1000_chunked.json"

print("Saved proccessed and chunked JSON files.")

with open(chunked_path, 'w', encoding='utf-8') as f:
    chunked_data = json.load()
    
docs = []

for chunk in chunked_data['chunks']:
    docs.append({
        'text': chunk['text'],
        'metadata': {
            'source_file': chunked_data['file_name'],
            'source_page': chunk['metadata']['source_page'],
            'chunk_id': chunk['metadata']['chunk_id']
        }
    })
    
save_dir = "faiss_store"
if Path(save_dir).exists():
    print("FAISS store already exists. Updating existing index.")
    db = VectorDB.load(save_dir=save_dir)
    db.add_documents(docs)
    db.save(save_dir=save_dir)
else:
    print("Creating new FAISS store.")
    db = VectorDB()
    db.add_documents(docs)
    db.save(save_dir=save_dir)
    
print("Vector DB updated and saved.")

"""
with open(chunked_path, 'w', encoding='utf-8') as f:
    json.dump(chunked_result, f, indent=2, ensure_ascii=False)

print(f"Done")"""
