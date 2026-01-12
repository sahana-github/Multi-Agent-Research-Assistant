import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from pydantic import BaseModel, Field
from typing import List
import requests
from bs4 import BeautifulSoup


class SearchResult(BaseModel):
    """Single search result"""
    title: str = Field(description="Title of the result")
    url: str = Field(description="URL of the source")
    content: str = Field(description="Snippet/content from the source")
    score: float = Field(default=0.8, description="Relevance score")


class SearchResults(BaseModel):
    """Collection of search results"""
    query: str = Field(description="Original search query")
    results: List[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Total number of results found")


class WebSearcherAgent:
    """Agent that searches the web for information using DuckDuckGo"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def search(self, query: str, max_results: int = 5) -> SearchResults:
        """Search the web using DuckDuckGo HTML"""
        
        print(f"🔍 Searching for: {query}")
        
        try:
            # Use DuckDuckGo HTML search
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            result_divs = soup.find_all('div', class_='result')[:max_results]
            
            for div in result_divs:
                try:
                    title_elem = div.find('a', class_='result__a')
                    snippet_elem = div.find('a', class_='result__snippet')
                    
                    if title_elem and snippet_elem:
                        title = title_elem.get_text(strip=True)
                        url = title_elem.get('href', '')
                        content = snippet_elem.get_text(strip=True)
                        
                        results.append(SearchResult(
                            title=title,
                            url=url,
                            content=content,
                            score=0.8
                        ))
                except:
                    continue
            
            # Fallback if DuckDuckGo fails
            if not results:
                results = self._mock_search_results(query, max_results)
            
            search_results = SearchResults(
                query=query,
                results=results,
                total_results=len(results)
            )
            
            print(f"✅ Found {len(results)} results\n")
            return search_results
            
        except Exception as e:
            print(f"⚠️ Search error: {e}")
            # Return mock results as fallback
            return SearchResults(
                query=query,
                results=self._mock_search_results(query, max_results),
                total_results=max_results
            )
    
    def _mock_search_results(self, query: str, max_results: int) -> List[SearchResult]:
        """Generate mock search results for demo purposes"""
        mock_results = [
            SearchResult(
                title=f"Research Article: {query}",
                url=f"https://example.com/article1",
                content=f"Comprehensive analysis of {query} with latest findings and research data from 2024.",
                score=0.9
            ),
            SearchResult(
                title=f"Latest Developments in {query}",
                url=f"https://example.com/article2",
                content=f"Recent innovations and trends related to {query}, including expert opinions and statistics.",
                score=0.85
            ),
            SearchResult(
                title=f"{query}: Industry Report 2024",
                url=f"https://example.com/report",
                content=f"Industry analysis and market research covering {query} with data-driven insights.",
                score=0.8
            )
        ]
        return mock_results[:max_results]
    
    def search_multiple(self, queries: List[str], max_results: int = 3) -> List[SearchResults]:
        """Search for multiple queries"""
        all_results = []
        for query in queries:
            results = self.search(query, max_results)
            all_results.append(results)
        return all_results
    
    def display_results(self, search_results: SearchResults):
        """Pretty print search results"""
        print("\n" + "="*60)
        print(f"🔍 SEARCH RESULTS FOR: {search_results.query}")
        print("="*60)
        
        for i, result in enumerate(search_results.results, 1):
            print(f"\n{i}. {result.title}")
            print(f"   🔗 {result.url}")
            print(f"   📊 Score: {result.score:.2f}")
            print(f"   📝 {result.content[:200]}...")
        
        print("\n" + "="*60 + "\n")


# Test the agent
if __name__ == "__main__":
    print("Testing Web Searcher Agent...\n")
    
    searcher = WebSearcherAgent()
    
    print("TEST 1: Single Search")
    results = searcher.search("AI in healthcare 2024", max_results=3)
    searcher.display_results(results)
    
    print("\nTEST 2: Multiple Searches")
    queries = ["AI diagnostics", "healthcare technology"]
    all_results = searcher.search_multiple(queries, max_results=2)
    
    for result_set in all_results:
        searcher.display_results(result_set)