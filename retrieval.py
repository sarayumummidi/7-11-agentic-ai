from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

#step 1: get the PDFs from where they are stored

#get the path of where the PDFs are stored in the directory 
pdf_dir = Path("data/Franke")
#each page for each PDF is loaded into memory as a document object, the document contains page content and metadata
#5 page manual = 5 document objects
all_docs = []


#step 2: load the pdfs page by page

#for every pdf file in the folder, PyPDFLoader reads the PDF and returns a list of documents
for pdf_file in pdf_dir.glob("*.pdf"):
    loader = PyPDFLoader(str(pdf_file))
    #each document has .page_content (text) and .metadata (dictionary) attribute 
    docs = loader.load()

    #attach the source filename to each documents metadata so we know where the text is from
    for doc in docs:
        #metadata will be saved with each chunk and returned the vector DB
        doc.metadata["source"] = pdf_file.name

    #finally you add all the page documents to the list
    all_docs.extend(docs)

print("Pages loaded:", len(all_docs))

# step 3: Split text into chunks

#we create a text splitter that makes chunks of about 400 tokens with a 50 token overlap
#the overlap helps to avoid cutting sentencees/ideas in half, so the retrieval is more robust
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

#split docs will hold the documents and their metadata, returning a new list of documents aka chunks
split_docs = text_splitter.split_documents(all_docs)
#print("Total chunks created:", len(split_docs))

# step 4: create a chroma vector db and embed the chunks 

#we want to create an embedded wrapper that chroma can call which will use the all-MiniLM-L6-v2 model
#chroma calls this function for each chunk and stores the resulting vectors 
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#now we build the chroma db for the documents(chunks). this will embed each chunk using the embedded function and
#store the vectors, text and metadate in a local directory called chroma_db
vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding_function,
    persist_directory="chroma_db"
)

#saves DB to disk allowing you to reload it later without having to recompute the embeddings
vectordb.persist()

#step 5: Test retrieval

#create a query question
query = "How do I descale Coffee Machine Model X?"

#similarity search runs a semantic search and returns te top k document chunks 
#each result being a document object with metadata and page content
results = vectordb.similarity_search(query, k=3)

#print the metadate and the first 200 characters of the returned chunk to inspect grounding
for res in results:
    print(res.metadata, res.page_content[:200], "...")




#what more needs to be done:
#1. Run OCR for PDF's that are scanned (images)
