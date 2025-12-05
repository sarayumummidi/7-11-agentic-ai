"""
This script builds a simple multi-agent pipeline that connects:
- A Planner Agent which decides what info is needed
- A Retriever Agent which pulls relevant chunks from FAISS
- A Synthesizer Agent that uses the LLM to create the final answer

the goal is to handle multi-step or cross-manual queries since we know that we can handle querying one document for information, just building up on that.
"""

import sys
from pathlib import Path
import os

#add the parent folder to Python's module search path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(PROJECT_ROOT))

from retrieval_backbone.VectorDB import VectorDB
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from config import MISTRAL_API_KEY
import os


#setup
os.environ["MISTRAL_API_KEY"] = MISTRAL_API_KEY

#load FAISS DB (in this case the multi-manual index)
FAISS_DIR = PROJECT_ROOT / "retrieval_backbone" / "faiss_store"
db = VectorDB.load(save_dir=str(FAISS_DIR))

#load mistral llm
llm = ChatMistralAI(model="mistral-large-latest", temperature=0.3)


def planner_agent(state):
    
    #understands what the user is asking, detects which manuals are mentioned (A1000, A300, etc.), creates a plan for the Retriever and Synthesizer agents
    question = state["question"]
    print(f"Planner thinking about: {question}")

    #default plan text
    if "compare" in question.lower():
        plan = "This seems like a comparison question. Retrieve info from all relevant manuals."
    else:
        plan = "Retrieve information from the manuals mentioned and summarize it clearly."

    #detect which manuals are mentioned in the question
    manuals_mentioned = []
    known_manuals = ["A1000", "A300", "A600", "S700"]

    for manual in known_manuals:
        if manual.lower() in question.lower():
            manuals_mentioned.append(manual)

    #if no manuals are found, assume all
    if not manuals_mentioned:
        manuals_mentioned = known_manuals  #search everything by default

    print(f"Manuals detected in query: {manuals_mentioned}")

    #return everything needed for the next step
    return {
        "plan": plan,
        "question": question,
        "manuals_mentioned": manuals_mentioned
    }



def retriever_agent(state):
    #searches the FAISS index for chunks that belong to the manuals detected by the Planner Agent

    question = state["question"]
    manuals_mentioned = state["manuals_mentioned"]
    print(f"Retriever fetching chunks for manuals: {manuals_mentioned}")

    # get all top results first
    results = db.search(question, k=15)

    #filter results by manual metadata
    filtered_results = [
        r for r in results
        if "manual" in r["metadata"]
        and any(m in r["metadata"]["manual"] for m in manuals_mentioned)
    ]

    #take the top 5 after filtering
    filtered_results = filtered_results[:5]

    #combine text for the LLM
    context = "\n\n".join([r["text"] for r in filtered_results])

    return {
        "question": question,
        "plan": state["plan"],
        "context": context,
        "manuals_mentioned": manuals_mentioned
    }



def synthesizer_agent(state):
    #enerates a final human-readable answer using the LLM
    print("Synthesizer writing final answer.....")

    prompt = ChatPromptTemplate.from_template("""
    You are an expert on Franke Coffee Systems.
    Based on the context below, answer the user’s question clearly and concisely.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """)

    chain = prompt | llm
    response = chain.invoke({
        "context": state["context"],
        "question": state["question"]
    })

    return {"final_answer": response.content}

#create the Graph (agent flow)
workflow = StateGraph(dict)

#add each agent as a node
workflow.add_node("planner", planner_agent)
workflow.add_node("retriever", retriever_agent)
workflow.add_node("synthesizer", synthesizer_agent)

#define the path (edges)
workflow.add_edge("planner", "retriever")
workflow.add_edge("retriever", "synthesizer")
workflow.add_edge("synthesizer", END)

#start the workflow
workflow.set_entry_point("planner")

#test
if __name__ == "__main__":
    user_question = "How do I safely clean the milk system in the A1000 and what hazards should I watch out for?" #"Compare the cleaning procedures of the A300 and A1000."
    result = workflow.compile().invoke({"question": user_question})

    print("\nFinal Answer:\n")
    print(result["final_answer"])
