#!/usr/bin/env python3
"""
SearXNG Integration for OB-1 AI Agent
Advanced integration with enhanced search capabilities for blockchain analysis
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from searxng_client import SearXNGClient

class OB1SearXNGIntegration:
    """Enhanced SearXNG integration for OB-1 AI Agent"""
    
    def __init__(self, config_path: str = None):
        """
        Initialize OB-1 SearXNG Integration
        
        Args:
            config_path: Path to SearXNG configuration file
        """
        self.config = self._load_config(config_path)
        self.client = SearXNGClient(
            base_url=self.config.get('base_url', 'https://search.example.com'),
            timeout=self.config.get('timeout', 30)
        )
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from JSON file
        
        Args:
            config_path: Path to config file
            
        Returns:
            Configuration dictionary
        """
        if not config_path:
            # Default configuration
            return {
                'base_url': os.getenv('SEARXNG_URL', 'https://search.example.com'),
                'timeout': 30,
                'default_engines': 'google,duckduckgo,bing',
                'blockchain_engines': 'google,duckduckgo,github'
            }
            
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    async def enhanced_search(self, 
                            query: str,
                            search_type: str = 'general',
                            max_results: int = 10) -> Dict[str, Any]:
        """
        Enhanced search with OB-1 specific optimizations
        
        Args:
            query: Search query
            search_type: Type of search (general, blockchain, documentation, security)
            max_results: Maximum number of results to return
            
        Returns:
            Enhanced search results with metadata
        """
        
        # Optimize query based on search type
        optimized_query = self._optimize_query(query, search_type)
        
        # Select appropriate engines
        engines = self._select_engines(search_type)
        
        # Perform search
        results = self.client.search(
            query=optimized_query,
            engines=engines,
            categories=self._get_categories(search_type)
        )
        
        # Enhance results with metadata
        enhanced_results = self._enhance_results(results, search_type, max_results)
        
        return enhanced_results
    
    def _optimize_query(self, query: str, search_type: str) -> str:
        """
        Optimize search query based on type
        
        Args:
            query: Original query
            search_type: Type of search
            
        Returns:
            Optimized query string
        """
        optimizations = {
            'blockchain': f"blockchain {query} OR crypto {query}",
            'documentation': f"{query} documentation OR {query} docs OR {query} API",
            'security': f"{query} security OR {query} audit OR {query} vulnerability",
            'defi': f"DeFi {query} OR decentralized finance {query}",
            'smart_contract': f"smart contract {query} OR solidity {query}"
        }
        
        return optimizations.get(search_type, query)
    
    def _select_engines(self, search_type: str) -> str:
        """
        Select appropriate search engines based on search type
        
        Args:
            search_type: Type of search
            
        Returns:
            Comma-separated engine list
        """
        engine_sets = {
            'blockchain': 'google,duckduckgo,github',
            'documentation': 'google,duckduckgo,github,stackoverflow',
            'security': 'google,duckduckgo,github',
            'general': 'google,duckduckgo,bing,startpage',
            'academic': 'google,duckduckgo,semantic_scholar'
        }
        
        return engine_sets.get(search_type, engine_sets['general'])
    
    def _get_categories(self, search_type: str) -> str:
        """
        Get appropriate search categories
        
        Args:
            search_type: Type of search
            
        Returns:
            Categories string
        """
        category_map = {
            'general': 'general',
            'blockchain': 'general',
            'documentation': 'general',
            'security': 'general',
            'images': 'images',
            'videos': 'videos',
            'news': 'news'
        }
        
        return category_map.get(search_type, 'general')
    
    def _enhance_results(self, 
                        results: Dict[str, Any], 
                        search_type: str, 
                        max_results: int) -> Dict[str, Any]:
        """
        Enhance search results with additional metadata and filtering
        
        Args:
            results: Raw search results
            search_type: Type of search
            max_results: Maximum results to return
            
        Returns:
            Enhanced results dictionary
        """
        if 'error' in results:
            return results
            
        enhanced = {
            'query': results.get('query', ''),
            'search_type': search_type,
            'total_results': results.get('number_of_results', 0),
            'results': [],
            'suggestions': results.get('suggestions', []),
            'metadata': {
                'engines_used': self._select_engines(search_type),
                'categories': self._get_categories(search_type),
                'enhanced': True
            }
        }
        
        # Process and filter results
        raw_results = results.get('results', [])
        for result in raw_results[:max_results]:
            enhanced_result = {
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'content': result.get('content', ''),
                'engine': result.get('engine', ''),
                'score': self._calculate_relevance_score(result, search_type),
                'metadata': {
                    'domain': self._extract_domain(result.get('url', '')),
                    'is_documentation': self._is_documentation_site(result.get('url', '')),
                    'is_official': self._is_official_site(result.get('url', ''))
                }
            }
            enhanced['results'].append(enhanced_result)
        
        # Sort by relevance score
        enhanced['results'].sort(key=lambda x: x['score'], reverse=True)
        
        return enhanced
    
    def _calculate_relevance_score(self, result: Dict[str, Any], search_type: str) -> float:
        """
        Calculate relevance score for a search result
        
        Args:
            result: Individual search result
            search_type: Type of search
            
        Returns:
            Relevance score (0-1)
        """
        score = 0.5  # Base score
        
        url = result.get('url', '').lower()
        title = result.get('title', '').lower()
        content = result.get('content', '').lower()
        
        # Boost for official sites
        if self._is_official_site(url):
            score += 0.3
            
        # Boost for documentation sites
        if self._is_documentation_site(url):
            score += 0.2
            
        # Boost for GitHub
        if 'github.com' in url:
            score += 0.15
            
        # Search type specific boosts
        if search_type == 'blockchain':
            blockchain_terms = ['ethereum', 'bitcoin', 'defi', 'smart contract', 'blockchain']
            for term in blockchain_terms:
                if term in title or term in content:
                    score += 0.1
                    
        return min(score, 1.0)
    
    def _extract_domain(self, url: str) -> str:
        """
        Extract domain from URL
        
        Args:
            url: Full URL
            
        Returns:
            Domain string
        """
        from urllib.parse import urlparse
        try:
            return urlparse(url).netloc
        except:
            return ''
    
    def _is_documentation_site(self, url: str) -> bool:
        """
        Check if URL is from a documentation site
        
        Args:
            url: URL to check
            
        Returns:
            True if documentation site
        """
        doc_indicators = ['docs.', 'documentation.', '/docs/', '/api/', '/guide/']
        return any(indicator in url.lower() for indicator in doc_indicators)
    
    def _is_official_site(self, url: str) -> bool:
        """
        Check if URL is from an official project site
        
        Args:
            url: URL to check
            
        Returns:
            True if likely official site
        """
        # Common official domains for blockchain projects
        official_domains = [
            'ethereum.org', 'bitcoin.org', 'uniswap.org', 'compound.finance',
            'aave.com', 'chainlink.link', 'polygon.technology'
        ]
        
        domain = self._extract_domain(url).lower()
        return any(official in domain for official in official_domains)

# Example usage
if __name__ == "__main__":
    # Initialize integration
    integration = OB1SearXNGIntegration()
    
    # Test enhanced search
    async def test_searches():
        # Test blockchain search
        blockchain_results = await integration.enhanced_search(
            "ethereum smart contracts", 
            search_type="blockchain"
        )
        print("Blockchain Search Results:")
        print(json.dumps(blockchain_results, indent=2))
        
        # Test documentation search
        doc_results = await integration.enhanced_search(
            "uniswap v3", 
            search_type="documentation"
        )
        print("\nDocumentation Search Results:")
        print(json.dumps(doc_results, indent=2))
    
    # Run tests
    asyncio.run(test_searches())
