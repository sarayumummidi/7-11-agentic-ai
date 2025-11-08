import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
import os
from config import MISTRAL_API_KEY
from VectorDB import VectorDB

os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

# load the FAISS vector DB
db = VectorDB.load(save_dir="faiss_store")

"""with open("A1000_chunked.json", "r", encoding="utf-8") as f:
    data = json.load(f)


all_chunks = [c["text"] for c in data["chunks"]]

context_text = "\n\n".join(all_chunks)"""

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.2,
)

prompt = ChatPromptTemplate.from_template("""
You are an expert technician and product trainer for Franke commercial coffee machines.
Here is the official Franke A1000 User Manual, which contains safety instructions, setup steps,
operating modes, cleaning procedures, configuration menus, troubleshooting tips,
and maintenance requirements. You will answer questions about this manual precisely
and only based on its contents.

First, find the quotes from the manual that are most relevant to answering the question,
and then list them in numbered order. Quotes should be short and directly relevant.

If no relevant quotes exist, write "No relevant quotes."

Then, answer the question, starting with "Answer:".
Do NOT copy the quotes verbatim inside the answer.
Instead, refer to them by their bracketed numbers at the end of relevant sentences.

Follow this exact format:

Quotes:
[1] "..."
[2] "..."

Answer:
Your summarized answer here, referring to quotes like [1], [2].

Focus on clarity, technical accuracy, and user safety when applicable.
If the question cannot be answered by the manual, state that directly.

-----------------
MANUAL CONTEXT:
{context}

USER QUESTION:
{question}
""")

chain = prompt | llm

user_question = "How do I safely clean the milk system and what hazards should I watch out for?"

response = chain.invoke({
    "context": context_text,
    "question": user_question
})

# debug 
print("\n--- Retreived Context Answer ---\n")
print(response.context_text[:1000])

print("\n--- Final Answer ---\n")
print(response.content)
