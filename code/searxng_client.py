#!/usr/bin/env python3
"""
SearXNG API Client
A Python client for interacting with SearXNG search API

Usage:
    client = SearXNGClient('https://your-searxng-instance.com')
    results = client.search('blockchain ethereum')
    
For OB-1 AI Agent integration
"""

import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlencode

class SearXNGClient:
    """Client for SearXNG API interactions"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize SearXNG client
        
        Args:
            base_url: Base URL of your SearXNG instance
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set user agent to avoid blocking
        self.session.headers.update({
            'User-Agent': 'OB-1-Agent/1.0 (Blockchain Analysis Bot)'
        })
    
    def search(self, 
               query: str,
               categories: str = 'general',
               engines: Optional[str] = None,
               lang: str = 'en',
               format_type: str = 'json',
               page: int = 1,
               **kwargs) -> Dict[str, Any]:
        """
        Perform search query
        
        Args:
            query: Search query string
            categories: Search categories (general, images, videos, news, etc.)
            engines: Specific engines to use (comma-separated)
            lang: Language code
            format_type: Response format (json, csv, rss)
            page: Page number for pagination
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing search results
        """
        params = {
            'q': query,
            'categories': categories,
            'lang': lang,
            'format': format_type,
            'pageno': page
        }
        
        if engines:
            params['engines'] = engines
            
        # Add any additional parameters
        params.update(kwargs)
        
        try:
            url = urljoin(self.base_url, '/search')
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            if format_type == 'json':
                return response.json()
            else:
                return {'content': response.text, 'format': format_type}
                
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'success': False}
    
    def get_suggestions(self, query: str) -> List[str]:
        """
        Get search suggestions
        
        Args:
            query: Partial search query
            
        Returns:
            List of suggestion strings
        """
        try:
            url = urljoin(self.base_url, '/autocompleter')
            params = {'q': query}
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return [f"Error getting suggestions: {str(e)}"]
    
    def search_blockchain(self, 
                         topic: str,
                         specific_protocol: Optional[str] = None) -> Dict[str, Any]:
        """
        Specialized search for blockchain-related topics
        
        Args:
            topic: Blockchain topic (defi, nft, smart contracts, etc.)
            specific_protocol: Specific protocol name if any
            
        Returns:
            Dictionary containing search results
        """
        query = f"blockchain {topic}"
        if specific_protocol:
            query += f" {specific_protocol}"
            
        # Use multiple engines for comprehensive results
        engines = 'google,duckduckgo,bing,startpage'
        
        return self.search(
            query=query,
            categories='general',
            engines=engines
        )
    
    def search_documentation(self, 
                           protocol_name: str,
                           doc_type: str = 'documentation') -> Dict[str, Any]:
        """
        Search for protocol documentation
        
        Args:
            protocol_name: Name of the protocol
            doc_type: Type of documentation (documentation, whitepaper, api, etc.)
            
        Returns:
            Dictionary containing search results
        """
        query = f"{protocol_name} {doc_type} site:docs OR site:github"
        
        return self.search(
            query=query,
            categories='general'
        )

# Example usage and testing
if __name__ == "__main__":
    # Example configuration
    SEARXNG_URL = "https://your-searxng-instance.com"  # Replace with your instance
    
    client = SearXNGClient(SEARXNG_URL)
    
    # Test basic search
    print("Testing basic search...")
    results = client.search("ethereum smart contracts")
    print(json.dumps(results, indent=2))
    
    # Test blockchain-specific search
    print("\nTesting blockchain search...")
    blockchain_results = client.search_blockchain("defi", "uniswap")
    print(json.dumps(blockchain_results, indent=2))
    
    # Test documentation search
    print("\nTesting documentation search...")
    doc_results = client.search_documentation("chainlink")
    print(json.dumps(doc_results, indent=2))
