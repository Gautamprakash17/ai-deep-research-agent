#!/usr/bin/env python3
"""
Quick test for Firecrawl API with provided key
"""

from firecrawl import FirecrawlApp

def test_firecrawl():
    """Test Firecrawl with the provided API key."""
    
    # Your Firecrawl API key
    api_key = "fc-da739b0d99ce4fd7ad9ea890fa7d0802"
    
    try:
        print("Testing Firecrawl API...")
        
        # Initialize FirecrawlApp
        firecrawl_app = FirecrawlApp(api_key=api_key)
        
        # Test 1: Basic URL scraping (updated for v1 API)
        print("\n1. Testing basic URL scraping...")
        test_url = "https://example.com"
        
        result = firecrawl_app.scrape_url(
            url=test_url
        )
        
        print(f"✅ Basic scraping successful!")
        print(f"   URL: {test_url}")
        if hasattr(result, 'title'):
            print(f"   Title: {result.title}")
        if hasattr(result, 'markdown'):
            content_length = len(result.markdown)
            print(f"   Content length: {content_length} characters")
            print(f"   Markdown preview: {result.markdown[:200]}...")
        if hasattr(result, 'html'):
            print(f"   HTML preview: {result.html[:200]}...")
        
        # Test 2: Search functionality (only supported parameters)
        print("\n2. Testing search functionality...")
        search_query = "artificial intelligence"
        
        search_result = firecrawl_app.search(
            query=search_query
        )
        print(f"✅ Search successful!")
        print(f"   Query: {search_query}")
        if hasattr(search_result, 'data'):
            print(f"   Results found: {len(search_result.data)}")
            if len(search_result.data) > 0:
                print(f"   First result: {search_result.data[0]}")
        else:
            print("   No results found in response")
        
        # Test 3: Deep research (updated for v1 API)
        print("\n3. Testing deep research (simplified)...")
        research_query = "machine learning"
        
        def on_activity(activity):
            print(f"   [{activity['type']}] {activity['message']}")
        
        research_result = firecrawl_app.deep_research(
            query=research_query,
            maxDepth=1,
            timeLimit=30,
            maxUrls=1,
            on_activity=on_activity
        )
        
        print(f"✅ Deep research successful!")
        print(f"   Query: {research_query}")
        
        if 'data' in research_result and 'sources' in research_result['data']:
            sources_count = len(research_result['data']['sources'])
            print(f"   Sources found: {sources_count}")
            
            if sources_count > 0:
                print(f"   First source: {research_result['data']['sources'][0].get('url', 'No URL')}")
        else:
            print("   No sources found in response")
        
        return True, "All Firecrawl tests passed"
        
    except Exception as e:
        print(f"❌ Firecrawl test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, str(e)

if __name__ == "__main__":
    print("=== Quick Firecrawl API Test ===\n")
    
    success, message = test_firecrawl()
    
    print(f"\n=== Test Results ===")
    print(f"Success: {success}")
    print(f"Message: {message}")
    
    if success:
        print("\n🎉 Firecrawl is working properly!")
        print("You can now use it for web scraping in your research agent.")
    else:
        print("\n⚠️  Firecrawl has issues. Check your API key and internet connection.") 