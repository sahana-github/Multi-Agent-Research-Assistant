from backend.agents.search_agent import search_agent
from backend.agents.rag_agent import rag_agent
from backend.agents.summarizer_agent import summarizer_agent

def search_node(state):
    return search_agent(state)

def rag_node(state):
    return rag_agent(state)

def summarizer_node(state):
    return summarizer_agent(state)