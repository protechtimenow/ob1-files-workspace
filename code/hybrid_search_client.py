#!/usr/bin/env python3
"""
Hybrid Search Client for OB-1
Combines SearXNG with fallback search methods for reliable search capabilities

This client provides:
1. SearXNG integration (when available)
2. Fallback to web search tools
3. Search result aggregation and ranking
4. Blockchain-optimized search patterns
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any, Union
from urllib.parse import urljoin, urlencode
from dataclasses import dataclass
from enum import Enum

class SearchMethod(Enum):
    SEARXNG = "searxng"
    WEB_SEARCH = "web_search"
    HYBRID = "hybrid"

@dataclass
class SearchResult:
    """Standardized search result format"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = None

class HybridSearchClient:
    """Enhanced search client with multiple fallback methods"""
    
    def __init__(self, searxng_url: Optional[str] = None, timeout: int = 30):
        """
        Initialize hybrid search client
        
        Args:
            searxng_url: Optional SearXNG instance URL
            timeout: Request timeout in seconds
        """
        self.searxng_url = searxng_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OB-1-Agent/1.0 (Blockchain Analysis Bot)'
        })
        
        # Track search method availability
        self.searxng_available = False
        self.last_searxng_check = 0
        self.check_interval = 300  # Check every 5 minutes
        
        if searxng_url:
            self._check_searxng_availability()
    
    def _check_searxng_availability(self) -> bool:
        """Check if SearXNG instance is available"""
        current_time = time.time()
        
        # Skip check if recently verified
        if current_time - self.last_searxng_check < self.check_interval:
            return self.searxng_available
        
        try:
            if self.searxng_url:
                response = self.session.get(self.searxng_url, timeout=5)
                self.searxng_available = response.status_code == 200
                self.last_searxng_check = current_time
                return self.searxng_available
        except requests.exceptions.RequestException:
            self.searxng_available = False
            self.last_searxng_check = current_time
        
        return False
    
    def _searxng_search(self, query: str, **kwargs) -> List[SearchResult]:
        """Perform search using SearXNG"""
        if not self.searxng_url or not self._check_searxng_availability():
            return []
        
        params = {
            'q': query,
            'categories': kwargs.get('categories', 'general'),
            'lang': kwargs.get('lang', 'en'),
            'format': 'json',
            'pageno': kwargs.get('page', 1)
        }
        
        engines = kwargs.get('engines')
        if engines:
            params['engines'] = engines
        
        try:
            url = urljoin(self.searxng_url, '/search')
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for result in data.get('results', []):
                search_result = SearchResult(
                    title=result.get('title', ''),
                    url=result.get('url', ''),
                    snippet=result.get('content', ''),
                    source='searxng',
                    metadata={'engine': result.get('engine', 'unknown')}
                )
                results.append(search_result)
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"SearXNG search failed: {e}")
            return []
    
    def _web_search_fallback(self, query: str, **kwargs) -> List[SearchResult]:
        """
        Fallback search method using available web search tools
        This is a placeholder - in actual OB-1 integration, this would call
        the web_search tool that's already available
        """
        # Placeholder for OB-1's web_search tool integration
        # In practice, this would call: await web_search([query])
        
        search_results = [
            SearchResult(
                title=f"Web Search Result for: {query}",
                url="https://example.com",
                snippet="This would contain actual search results from OB-1's web search tool",
                source="web_search_tool",
                relevance_score=0.8
            )
        ]
        
        return search_results
    
    def search(self, 
               query: str,
               method: SearchMethod = SearchMethod.HYBRID,
               max_results: int = 10,
               **kwargs) -> List[SearchResult]:
        """
        Perform search using specified or best available method
        
        Args:
            query: Search query string
            method: Preferred search method
            max_results: Maximum number of results to return
            **kwargs: Additional search parameters
            
        Returns:
            List of SearchResult objects
        """
        all_results = []
        
        if method in [SearchMethod.SEARXNG, SearchMethod.HYBRID]:
            # Try SearXNG first
            searxng_results = self._searxng_search(query, **kwargs)
            all_results.extend(searxng_results)
        
        if method in [SearchMethod.WEB_SEARCH, SearchMethod.HYBRID]:
            # Use web search if SearXNG failed or as supplement
            if not all_results or method == SearchMethod.HYBRID:
                web_results = self._web_search_fallback(query, **kwargs)
                all_results.extend(web_results)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result.url not in seen_urls:
                seen_urls.add(result.url)
                unique_results.append(result)
        
        # Sort by relevance and limit results
        unique_results.sort(key=lambda x: x.relevance_score, reverse=True)
        return unique_results[:max_results]
    
    def search_blockchain(self, 
                         topic: str,
                         protocol: Optional[str] = None,
                         search_type: str = "general") -> List[SearchResult]:
        """
        Specialized blockchain search with optimized queries
        
        Args:
            topic: Blockchain topic (defi, nft, smart contracts, etc.)
            protocol: Specific protocol name
            search_type: Type of search (general, documentation, security, etc.)
            
        Returns:
            List of SearchResult objects
        """
        # Build optimized query
        query_parts = ["blockchain", topic]
        if protocol:
            query_parts.append(protocol)
        
        # Add search type specific terms
        if search_type == "documentation":
            query_parts.extend(["docs", "documentation", "whitepaper"])
        elif search_type == "security":
            query_parts.extend(["security", "audit", "vulnerability"])
        elif search_type == "analysis":
            query_parts.extend(["analysis", "review", "research"])
        
        query = " ".join(query_parts)
        
        # Use blockchain-optimized search parameters
        kwargs = {
            'engines': 'google,duckduckgo,bing',
            'categories': 'general'
        }
        
        return self.search(query, method=SearchMethod.HYBRID, **kwargs)
    
    def search_smart_contract(self, 
                            contract_address: str,
                            chain: str = "ethereum") -> List[SearchResult]:
        """
        Search for information about a specific smart contract
        
        Args:
            contract_address: Contract address to search for
            chain: Blockchain name
            
        Returns:
            List of SearchResult objects
        """
        query = f"{chain} smart contract {contract_address} etherscan"
        
        kwargs = {
            'engines': 'google,duckduckgo',
            'categories': 'general'
        }
        
        return self.search(query, method=SearchMethod.HYBRID, **kwargs)
    
    def get_search_status(self) -> Dict[str, Any]:
        """Get status of available search methods"""
        return {
            'searxng': {
                'configured': self.searxng_url is not None,
                'available': self.searxng_available,
                'url': self.searxng_url,
                'last_checked': self.last_searxng_check
            },
            'web_search_fallback': {
                'available': True,
                'description': 'OB-1 built-in web search tool'
            },
            'recommended_method': SearchMethod.HYBRID.value
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize with optional SearXNG URL
    client = HybridSearchClient("https://your-searxng-instance.com")
    
    # Check status
    print("Search Status:")
    status = client.get_search_status()
    print(json.dumps(status, indent=2, default=str))
    
    # Test blockchain search
    print("\nTesting blockchain search...")
    results = client.search_blockchain("defi", "uniswap", "documentation")
    
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. {result.title}")
        print(f"   URL: {result.url}")
        print(f"   Source: {result.source}")
        print(f"   Snippet: {result.snippet[:100]}...")
    
    # Test smart contract search
    print("\nTesting smart contract search...")
    contract_results = client.search_smart_contract(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
        "ethereum"
    )
    
    for result in contract_results[:2]:
        print(f"- {result.title}")
        print(f"  {result.url}")