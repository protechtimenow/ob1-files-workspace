# SearXNG API Integration Setup Guide

## Overview

This guide helps you set up SearXNG API integration for enhanced private search capabilities with OB-1 AI Agent.

## What is SearXNG?

SearXNG is a free internet metasearch engine that aggregates results from various search services and databases. It provides:
- **Privacy-focused search** - No tracking or data collection
- **Multiple engine aggregation** - Combines results from Google, Bing, DuckDuckGo, etc.
- **Self-hostable** - Run your own private search instance
- **API access** - Programmatic access to search functionality

## Setup Steps

### 1. SearXNG Instance Setup

#### Option A: Use Public Instance
```bash
# Find public instances at: https://searx.space/
# Example public instances:
# - https://searx.be
# - https://search.sapti.me
# - https://searx.prvcy.eu
```

#### Option B: Self-Host (Recommended for Production)
```bash
# Using Docker (easiest method)
git clone https://github.com/searxng/searxng-docker.git
cd searxng-docker

# Edit .env file with your settings
cp env.example .env

# Start SearXNG
docker-compose up -d
```

### 2. Configuration

#### Update Configuration File
Edit `config-files/searxng-config.json` with your instance details:

```json
{
  "base_url": "https://your-searxng-instance.com",
  "timeout": 30,
  "default_engines": "google,duckduckgo,bing",
  "blockchain_engines": "google,duckduckgo,github"
}
```

#### Environment Variables
Set these environment variables:

```bash
export SEARXNG_URL="https://your-searxng-instance.com"
export SEARXNG_TIMEOUT=30
```

### 3. Installation

#### Install Dependencies
```bash
pip install requests asyncio
```

#### Test Installation
```bash
python3 code/searxng_client.py
```

### 4. OB-1 Integration

#### Basic Usage
```python
from code.searxng_integration import OB1SearXNGIntegration

# Initialize
integration = OB1SearXNGIntegration('config-files/searxng-config.json')

# Search
results = await integration.enhanced_search("ethereum defi", search_type="blockchain")
```

#### Advanced Features

**Blockchain-Specific Search:**
```python
# Search for DeFi protocols
defi_results = await integration.enhanced_search(
    "liquidity pools", 
    search_type="blockchain"
)

# Search for documentation
doc_results = await integration.enhanced_search(
    "uniswap v3 whitepaper", 
    search_type="documentation"
)

# Security-focused search
security_results = await integration.enhanced_search(
    "smart contract vulnerabilities", 
    search_type="security"
)
```

## API Endpoints

### Search Endpoint
```
GET /search?q={query}&categories={categories}&engines={engines}&format=json
```

**Parameters:**
- `q` (required): Search query
- `categories`: Search categories (general, images, videos, news)
- `engines`: Specific engines to use
- `format`: Response format (json, csv, rss)
- `lang`: Language code
- `pageno`: Page number

### Autocomplete Endpoint
```
GET /autocompleter?q={partial_query}
```

## Response Format

### JSON Response Structure
```json
{
  "query": "ethereum smart contracts",
  "number_of_results": 150,
  "results": [
    {
      "title": "Ethereum Smart Contracts Guide",
      "url": "https://ethereum.org/en/developers/docs/smart-contracts/",
      "content": "Smart contracts are programs stored on blockchain...",
      "engine": "google",
      "category": "general"
    }
  ],
  "suggestions": ["ethereum smart contract tutorial", "ethereum solidity"]
}
```

## Best Practices

### Performance Optimization
- **Engine Selection**: Choose engines based on search type
- **Result Limiting**: Set reasonable limits for number of results
- **Caching**: Implement result caching for repeated queries
- **Rate Limiting**: Respect instance rate limits

### Search Query Optimization
- **Specific Terms**: Use specific blockchain terminology
- **Site Filtering**: Use `site:github.com` for code searches
- **Boolean Operators**: Use AND, OR, NOT for precise results
- **Quotes**: Use quotes for exact phrase matching

### Privacy Considerations
- **No Tracking**: SearXNG doesn't track or store searches
- **Self-Hosting**: Host your own instance for maximum privacy
- **HTTPS**: Always use HTTPS connections
- **Log Management**: Configure appropriate logging levels

## Troubleshooting

### Common Issues

**Connection Errors:**
```python
# Check instance status
response = requests.get(f"{searxng_url}/stats")
print(f"Status: {response.status_code}")
```

**Rate Limiting:**
```python
# Implement backoff strategy
import time
time.sleep(1)  # Add delay between requests
```

**Empty Results:**
- Check if engines are working
- Try different engine combinations
- Verify query formatting

### Debug Mode
Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Integration Examples

### Blockchain Protocol Research
```python
# Research a specific protocol
protocol_results = await integration.enhanced_search(
    "Aave lending protocol technical documentation",
    search_type="documentation",
    max_results=10
)

# Analyze results
for result in protocol_results['results']:
    if result['metadata']['is_official']:
        print(f"Official docs: {result['url']}")
```

### Smart Contract Analysis
```python
# Search for contract implementations
contract_results = await integration.enhanced_search(
    "ERC-20 token implementation solidity",
    search_type="smart_contract",
    max_results=15
)

# Filter GitHub results
github_results = [
    r for r in contract_results['results'] 
    if 'github.com' in r['url']
]
```

### Security Research
```python
# Search for security issues
security_results = await integration.enhanced_search(
    "reentrancy attack smart contract",
    search_type="security",
    max_results=20
)

# Prioritize high-score results
top_results = [
    r for r in security_results['results'] 
    if r['score'] > 0.8
]
```

## Advanced Configuration

### Custom Engine Configuration
```json
{
  "engines": {
    "blockchain_research": "google,duckduckgo,github,stackoverflow",
    "documentation": "google,duckduckgo,github",
    "security_analysis": "google,duckduckgo,cve_search"
  },
  "categories": {
    "code": "it",
    "research": "science",
    "news": "news"
  }
}
```

### Result Processing Pipeline
```python
class CustomResultProcessor:
    def process_results(self, results):
        # Custom filtering logic
        # Relevance scoring
        # Content extraction
        # Metadata enhancement
        pass
```

## Resources

- [SearXNG Official Documentation](https://docs.searxng.org/)
- [SearXNG GitHub Repository](https://github.com/searxng/searxng)
- [Public SearXNG Instances](https://searx.space/)
- [SearXNG Docker Setup](https://github.com/searxng/searxng-docker)

## Support

For issues with this integration:
1. Check the troubleshooting section
2. Verify your SearXNG instance is running
3. Test with simple queries first
4. Check API endpoint responses manually

---

**Note**: Replace `your-searxng-instance.com` with your actual SearXNG instance URL throughout the configuration files.
