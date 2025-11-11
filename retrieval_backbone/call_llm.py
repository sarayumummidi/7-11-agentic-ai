#this script connects our FAISS vector database to the Mistral AI model.
#it retrieves the top relevant chunks from the Franke A1000 manual,
#and passes those chunks as context to the model to answer a user's question


import os
import json
#used to structure our LLM prompt
from langchain_core.prompts import ChatPromptTemplate
#connects to the Mistral API
from langchain_mistralai import ChatMistralAI
#import API key from your config file
from config import MISTRAL_API_KEY
#our custom FAISS-based vector DB class
from VectorDB import VectorDB


#step 1: step up api key and load faiss

#this makes sure your Mistral API key is accessible to LangChain
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

#load the FAISS vector database that we created earlier
#(this contains all 92 embedded chunks from the A1000 manual)
db = VectorDB.load(save_dir="faiss_store")

#step 2: set up the LLM model

#initialize the Mistral model you want to use
#mistral-large-latest is large, high-quality model for accurate answers
llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.2,   # lower = more focused, deterministic answers
)

#step 3: define prompt template

prompt = ChatPromptTemplate.from_template("""
You are an expert technician and product trainer for Franke commercial coffee machines.
Here is the official Franke A1000 User Manual, which contains safety instructions,
setup steps, operating modes, cleaning procedures, configuration menus,
troubleshooting tips, and maintenance requirements.

Your task: answer the user's question based only on the manual content provided.

First, find the quotes from the manual that are most relevant to answering the question,
and then list them in numbered order. Quotes should be short and directly relevant.

If no relevant quotes exist, write "No relevant quotes."

Then, answer the question, starting with "Answer:".
Do NOT copy the quotes verbatim inside the answer.
Instead, refer to them by their bracketed numbers at the end of relevant sentences.

Format your answer exactly like this:

Quotes:
[1] "..."
[2] "..."

Answer:
Your summarized answer here, referring to quotes like [1], [2].

Be precise, safe, and technically clear.
If the question cannot be answered by the manual, say so.

-----------------
MANUAL CONTEXT:
{context}

USER QUESTION:
{question}
""")

#step 4: define the chain (prompt -> model)

chain = prompt | llm

#step 5: sample question

user_question = "How do I safely clean the milk system and what hazards should I watch out for?"

#retrieve top 5 most relevant chunks from the FAISS store
results = db.search(user_question, k=5)

#combine all the retrieved chunks into one context string
#separate them with two newlines (\n\n) to help the model read them clearly
context_text = "\n\n".join([r["text"] for r in results])

#step 6: run the query through the llm

#feed both the question and the retrieved context into the model.
response = chain.invoke({
    "context": context_text,
    "question": user_question
})


#step 7: print the result
#this helps to see both the chunks retrieved and the model’s final answer.
print("\n--- Retrieved Context (First 1000 chars) ---\n")
print(context_text[:1000])  #print first 1000 chars for readability
print("\n--- Final Answer from Mistral ---\n")
print(response.content)