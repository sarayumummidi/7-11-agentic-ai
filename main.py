# main.py
from fastapi import FastAPI
from agentic_reasoning.multi_agent_pipeline import workflow, stream_synthesizer_agent
from pydantic import BaseModel
from fastapi import WebSocket
import asyncio

class Question(BaseModel):
    question: str

# Compile the workflow once at module level
pipeline_app = workflow.compile()

# Create FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "7-11 Agentic AI API",
        "endpoints": {
            "POST /ask": "Ask a question (requires JSON body with 'question' field)",
            "POST /stream": "Stream the answer to a question (websocket)"
        }
    }


@app.post("/ask")
async def ask(question: Question):
    result = pipeline_app.invoke({"question": question.question})
    return {"answer": result["final_answer"]}

@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    try:
        # Frontend sends the question through the websocket
        data = await websocket.receive_json()
        question = data["question"]

        # Step 1: Run pipeline up to retriever to get context
        # (Planner → Retriever to get relevant chunks)
        context = None
        
        for event in pipeline_app.stream({"question": question}):
            for node_name, node_output in event.items():
                if node_name == "retriever" and isinstance(node_output, dict):
                    context = node_output.get("context", "")
                    break
            if context is not None:
                break

        # Step 2: Stream LLM response token-by-token using the synthesizer streaming function
        async for content in stream_synthesizer_agent(context, question):
            try:
                # Send each token/chunk to frontend as it arrives
                await websocket.send_text(content)
            except:
                # Connection closed by client, stop streaming
                break

    except Exception as e:
        # Try to send error, but don't fail if connection is closed
        try:
            await websocket.send_text(f"Error: {str(e)}")
        except:
            pass

    
