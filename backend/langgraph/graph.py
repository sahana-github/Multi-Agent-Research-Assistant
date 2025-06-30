from langgraph.graph import StateGraph,END
from backend.agents.search_agent import search_agent
from backend.agents.summarizer_agent import summarizer_agent
from backend.agents.controller_agent import controller_agent
from typing import TypedDict

class ContextState(TypedDict):
    context:dict


graph=StateGraph(ContextState)

graph.add_node("controller", controller_agent)
graph.add_node("search", search_agent)
graph.add_node("summarizer", summarizer_agent)

graph.set_entry_point("controller")
graph.add_edge("controller", "search")
graph.add_edge("search", "summarizer")
graph.add_edge("summarizer", END)


dag=graph.compile()