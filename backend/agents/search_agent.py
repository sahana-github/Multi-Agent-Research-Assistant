import requests
import xml.etree.ElementTree as ET

def search_arxiv(query,max_results=3):
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }
    response = requests.get(base_url, params=params)
    return response.text

def parse_arxiv_response(xml_data):
    root=ET.fromstring(xml_data)
    ns={'atom': 'http://www.w3.org/2005/Atom'}
    entries=root.findall('atom:entry', ns)
    results=[]  
    for entry in entries:
        title=entry.find('atom:title', ns).text.strip()
        summary=entry.find('atom:summary', ns).text.strip()
        link=entry.find('atom:id', ns).text.strip()
        results.append({
            "title": title,
            "summary": summary,
            "url": link
        })
    return results

def search_agent(state):
    user_query=state["context"]["user_query"]

    xml_data=search_arxiv(user_query)
    results=parse_arxiv_response(xml_data)

    state["context"]["search_results"]=results
    return state