from langchain_ollama import OllamaLLM as Ollama


llm=Ollama(model="mistral")

def summarizer_agent(state):
    result=state["context"].get("search_results", [])

    if not result:
        state["context"]["summary"] = "No search results found."
        return state
    
    top_paper=result[0]
    text=f"Title: {top_paper['title']}\nAbstarct: {top_paper['summary']}\n\nUSummarise this in 3-4 "
    
    
    summary=llm.invoke(text)


    state["context"]["summary"] = summary.strip()
    return state