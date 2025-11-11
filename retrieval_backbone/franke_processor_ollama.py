#used to work with file and folder paths in a clean way
from pathlib import Path
#lets us handle images when we need OCR
from PIL import Image
#lets us extract text from images
import pytesseract
#LangChain utility to break long text into smaller chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
#database for storing and searching vector embeddings
from langchain_community.vectorstores import FAISS
#generates embeddings (numeric vectors that capture meaning of text)
from langchain_community.embeddings import SentenceTransformerEmbeddings
#allows us to call local LLMs
from langchain_community.llms import Ollama
#LangChain wrapper to combine retrieval + LLM answering
from langchain.chains import RetrievalQA

#very accurate PDF parser, extracts text directly from PDF pages (better than MyPDFLoader)
import fitz




#step 1: load and extract the text from the PDF

#get the path to the specific PDF we want to test with
pdf_dir = Path("data/Franke/20109399_User manual_A1000_en.pdf")
#open the PDF with PyMuPDF
doc = fitz.open(pdf_dir)


#store extracted text from each page in a list
pages_text = []

#loop through every page in the PDF
for page in doc:
    #try extracting the text directly (works for PDFs that have selectable text)
    text = page.get_text()
    #if the page is an image with no text or just blank
    if not text.strip():  
        # convert the page to an image using PyMUPDF
        pix = page.get_pixmap()
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        #run OCR with pytesseract on the image to extract the text in the picture and turn it into a string
        text = pytesseract.image_to_string(image)
    #save the text (whether from PDF or OCR)
    pages_text.append(text)

#turn the pages text into one long string of text
full_text = "\n".join(pages_text)




# step 2: Split text into chunks

#we create a text splitter that makes chunks of about 500 tokens with a 100 token overlap
#the overlap helps to avoid cutting sentences/ideas in half, so the retrieval is more robust
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100   #increased it to make sure context is not lost at the boundaries
)

#apply the splitter to our full pdf text
chunks = text_splitter.create_documents([full_text])




# step 3: create a chroma vector db and embed the chunks (embeddings + store in FAISS)

#we want to create an embedded wrapper that chroma can call which will use the all-MiniLM-L6-v2 model
#chroma calls this function for each chunk and stores the resulting vectors 
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#FAISS stores all the embeddings so we can quickly search by meaning instead of keywords
vectordb = FAISS.from_documents(chunks, embedding_function)




#step 4: connect ollama for Q&A

#load a local language model through Ollama

#we are using 8B parameter LLaMA 3 model but might switch to a different one
llm = Ollama(model="phi3:3.8b")

#create a retriever that pulls the top 5 most relevant chunks from FAISS
retriever = vectordb.as_retriever(search_kwargs={"k":5})

#this will help us debug the chunks for a specified sample query
results = retriever.get_relevant_documents("Explain the 5-step cleaning method of the A1000")
for i, r in enumerate(results, 1):
    print(f"\nChunk {i}")
    print(r.page_content[:500])  # first 500 chars of each chunk







#step 5: build retrieval QA chain


#build a qa that: uses FAISS to find relevant text chunks, passes those chunks to Ollama model, then ollama generates a human-readable answer 
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)



#step 6; test the pipeline with a query 

#create a query question
query = "Explain the 5-step cleaning method of the A1000"

#run the query through our RetrievalQA chain
answer = qa.run(query)

#print the result
print("Question:", query)
print("Answer:", answer)
