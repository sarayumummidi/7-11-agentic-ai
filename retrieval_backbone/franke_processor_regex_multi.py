#multi manual pipleine


import sys
from pathlib import Path

# Path setup and add parent folder so imports from retrieval_backbone work

THIS_DIR = Path(__file__).resolve().parent # .../retrieval_backbone
PROJECT_ROOT = THIS_DIR.parent # repo root (one level up)

sys.path.append(str(THIS_DIR))

#import the FrankePDFProcessor class
from franke_processor_regex import FrankePDFProcessor
from VectorDB import VectorDB
import json

#folder containing all your raw Franke manuals
pdf_dir = PROJECT_ROOT / "data" / "raw"

#where to save processed outputs
# Processed JSONs go here
output_dir = PROJECT_ROOT / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

#save to faiss vector db
save_dir = THIS_DIR / "faiss_store"


def main():
    #initialize the processor
    processor = FrankePDFProcessor(target_tokens=400, overlap_tokens=50)

    #iterate through all PDFs in the folder
    all_docs = []
    for pdf_path in pdf_dir.glob("*.pdf"):
        print(f"\n Processing manual: {pdf_path.name}")

        #extract and chunk text
        processed_result, chunked_result = processor.process_franke_pdf(pdf_path)

        #save individual JSONs for each pdf
        processed_path = output_dir / f"{pdf_path.stem}_processed.json"
        chunked_path = output_dir / f"{pdf_path.stem}_chunked.json"

        with open(processed_path, 'w', encoding='utf-8') as f:
            json.dump(processed_result, f, indent=2, ensure_ascii=False)

        with open(chunked_path, 'w', encoding='utf-8') as f:
            json.dump(chunked_result, f, indent=2, ensure_ascii=False)

        #add chunks to combined document list
        for chunk in chunked_result["chunks"]:
            #try to extract the model name (like "A1000") from the file name
            file_name = chunked_result["file_name"]
            if "A1000" in file_name:
                manual_name = "A1000"
            elif "A300" in file_name:
                manual_name = "A300"
            elif "A600" in file_name:
                manual_name = "A600"
            elif "S700" in file_name:
                manual_name = "S700"
            else:
                manual_name = "Unknown"

            all_docs.append({
                "text": chunk["text"],
                "metadata": {
                    "source_file": chunked_result["file_name"],
                    "manual": manual_name,
                    "source_page": chunk["metadata"]["source_page"],
                    "chunk_id": chunk["metadata"]["chunk_id"]
                }
            })


    # Save to FAISS
    if save_dir.exists() and (save_dir / "index.bin").exists():
        print("\nFAISS store exists, updating with new manuals.....")
        db = VectorDB.load(save_dir=save_dir)
        db.add_documents(all_docs)
    else:
        print("\nCreating new FAISS store for all manuals...")
        save_dir.mkdir(parents=True, exist_ok=True)
        db = VectorDB()
        db.add_documents(all_docs)

    db.save(save_dir=save_dir)
    print("\nMulti-manual FAISS database updated and saved successfully")

if __name__ == "__main__":
    main()
