from fastapi import FastAPI
from pydantic import BaseModel
from backend.workflow_engine.workflow import dag
from backend.mcp.context_schema import get_initial_context

app = FastAPI()

class QueryRequest(BaseModel):
    user_input: str
    modality: str

@app.post("/ask")
async def ask_query(data: QueryRequest):
    context = get_initial_context(data.user_input, data.modality)
    final_state = dag.invoke(context)
    answer = final_state["context"].get("summary", "No answer generated")
    return {"response": answer}
