from langgraph.graph import StateGraph, END
from backend.agents.controller_agent import search_node, rag_node, summarizer_node

graph = StateGraph(dict)
graph.add_node("search", search_node)
graph.add_node("rag", rag_node)
graph.add_node("summarizer", summarizer_node)

graph.set_entry_point("search")
graph.add_edge("search", "rag")
graph.add_edge("rag", "summarizer")
graph.add_edge("summarizer", END)

dag = graph.compile()