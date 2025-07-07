from langchain_community.llms import Ollama
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

llm = Ollama(model="llama2")

prompt_template = PromptTemplate(
    input_variables=["content"],
    template="""You are a helpful AI. Summarize the following:

    {content}

    Summary:"""
)

def summarizer_agent(state):
    content = (
        state["context"].get("search_results", "") +
        "\n\n" +
        state["context"].get("rag_results", "")
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    summary = chain.run(content)
    state["context"]["summary"] = summary
    return state
