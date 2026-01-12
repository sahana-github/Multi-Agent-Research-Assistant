from langchain_community.tools import DuckDuckGoSearchRun

def search_agent(state):
    query = state["context"]["user_query"]
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    state["context"]["search_results"] = results
    return state
