from fastapi import FastAPI,Request
from pydantic import BaseModel
from backend.langgraph.graph import dag
from backend.mcp.context_schema import get_initial_context

app = FastAPI()

class QueryRequest(BaseModel):
    user_input:str
    modality:str="text"

@app.post("/ask")
async def ask_query(data:QueryRequest):
    final_state=dag.invoke(context)

    answer=final_state["context"].get("summary","No answer generated")
    return {"response":answer}
