import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from tavily import TavilyClient
from pydantic import BaseModel, Field
from typing import List
from utils.config import Config


class SearchResult(BaseModel):
    """Single search result"""
    title: str = Field(description="Title of the result")
    url: str = Field(description="URL of the source")
    content: str = Field(description="Snippet/content from the source")
    score: float = Field(default=0.0, description="Relevance score")


class SearchResults(BaseModel):
    """Collection of search results"""
    query: str = Field(description="Original search query")
    results: List[SearchResult] = Field(description="List of search results")
    total_results: int = Field(description="Total number of results found")


class WebSearcherAgent:
    """Agent that searches the web for information"""
    
    def __init__(self):
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    
    def search(self, query: str, max_results: int = 5) -> SearchResults:
        """Search the web for information"""
        
        print(f"🔍 Searching for: {query}")
        
        # Perform search using Tavily
        response = self.client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"  # Use advanced search for better results
        )
        
        # Parse results
        results = []
        for item in response.get('results', []):
            results.append(SearchResult(
                title=item.get('title', 'No title'),
                url=item.get('url', ''),
                content=item.get('content', ''),
                score=item.get('score', 0.0)
            ))
        
        search_results = SearchResults(
            query=query,
            results=results,
            total_results=len(results)
        )
        
        print(f"✅ Found {len(results)} results\n")
        
        return search_results
    
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
    
    # Create agent
    searcher = WebSearcherAgent()
    
    # Test single search
    print("TEST 1: Single Search")
    results = searcher.search("AI in healthcare 2024 innovations", max_results=3)
    searcher.display_results(results)
    
    # Test multiple searches
    print("\nTEST 2: Multiple Searches")
    queries = [
        "FDA approved AI medical devices 2024",
        "AI diagnostic tools healthcare"
    ]
    
    all_results = searcher.search_multiple(queries, max_results=2)
    
    for result_set in all_results:
        searcher.display_results(result_set)
    
    # Show raw data
    print("Raw Data Sample:")
    print(results.model_dump_json(indent=2))