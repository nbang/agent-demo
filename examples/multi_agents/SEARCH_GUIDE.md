# 🔍 Improving DuckDuckGo Search Reliability in Multi-Agent Systems

This guide addresses common issues with DuckDuckGo Tools (DDGT) and provides robust solutions for web search in your multi-agent examples.

## 🚨 Common Issues with DuckDuckGo Search

### Rate Limiting and Blocking
- **Problem**: DuckDuckGo blocks requests when too many are made too quickly
- **Symptoms**: `HTTP 429 Too Many Requests`, connection timeouts, empty results
- **Impact**: Agents fail to gather web information, breaking multi-agent workflows

### Network Instability
- **Problem**: Temporary network issues or DNS problems
- **Symptoms**: `ConnectionError`, `TimeoutError`, intermittent failures
- **Impact**: Inconsistent agent performance

### Anti-Bot Detection
- **Problem**: DuckDuckGo detects automated requests and blocks them
- **Symptoms**: Empty results, `HTTP 403 Forbidden`, captcha challenges
- **Impact**: Search functionality completely breaks

## ✅ Solution: Robust Search Tools

I've created an improved search system with three modes:

### 1. Robust Mode (Recommended)
```python
from search_config import get_search_tools

# Use in your agents
tools=[get_search_tools("robust")]
```

**Features:**
- ✅ Automatic retries with exponential backoff
- ✅ Rate limiting (waits between requests)
- ✅ Error handling with graceful fallbacks
- ✅ Logging for debugging
- ✅ Fallback responses when search fails

### 2. Mock Mode (For Testing)
```python
tools=[get_search_tools("mock")]
```

**Features:**
- ✅ Realistic mock data (no network required)
- ✅ Perfect for testing multi-agent workflows
- ✅ Consistent results for demonstrations
- ✅ No rate limits or network issues

### 3. Original Mode (Use with Caution)
```python
tools=[get_search_tools("original")]
```

**Features:**
- ⚡ Fast when working
- ❌ No error handling
- ❌ Fails with rate limits

## 🛠️ Configuration Options

### Environment Variables
```bash
# Set search mode globally
export SEARCH_MODE=robust        # Default: robust error handling
export SEARCH_MODE=mock          # Use mock data for testing
export SEARCH_MODE=original      # Original DuckDuckGo (risky)

# Adjust retry behavior
export SEARCH_MAX_RETRIES=3      # Max retry attempts
export SEARCH_BASE_DELAY=1.0     # Base delay between retries
export SEARCH_MIN_INTERVAL=2.0   # Minimum seconds between requests
```

### In PowerShell (Windows)
```powershell
$env:SEARCH_MODE="robust"
$env:SEARCH_MAX_RETRIES="5"
```

## 🎯 Implementation in Your Agents

### Before (Problematic)
```python
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    name="Research Agent",
    tools=[DuckDuckGoTools()],  # May fail with rate limits
    # ...
)
```

### After (Robust)
```python
from search_config import get_search_tools

agent = Agent(
    name="Research Agent", 
    tools=[get_search_tools()],  # Handles errors gracefully
    # ...
)
```

## 🧪 Testing Your Setup

### Quick Test
```bash
cd examples/multi_agents
python quick_test.py
```

### Configuration Check
```bash
python search_config.py
```

### Test All Modes
```bash
python test_search_tools.py
```

## 📊 Error Handling Strategy

### Robust Mode Behavior
1. **First Attempt**: Try normal search with rate limiting
2. **Retry Logic**: If failed, wait and retry with exponential backoff
3. **Fallback Response**: If all retries fail, provide helpful fallback message
4. **Logging**: Track all attempts for debugging

### Example Fallback Response
When search fails completely, agents receive:
```json
{
  "title": "Search Service Unavailable",
  "body": "Web search is currently unavailable. Please use existing knowledge base for this topic and note that current web data is not available.",
  "href": "https://example.com"
}
```

## 🔧 Customizing Error Handling

### Adjust Retry Parameters
```python
from robust_search_tools import RobustWebSearchTools

# Custom configuration
custom_tools = RobustWebSearchTools(
    max_retries=5,           # More retries
    base_delay=2.0,          # Longer delays
)
```

### Custom Fallback Responses
Modify `_get_fallback_response()` in `robust_search_tools.py` to customize what agents receive when search fails.

## 🚀 Best Practices

### 1. Use Robust Mode by Default
```python
# Always use robust mode for production
tools=[get_search_tools("robust")]
```

### 2. Test with Mock Mode First
```bash
# Test your multi-agent logic without network issues
export SEARCH_MODE=mock
python your_agent_script.py
```

### 3. Monitor Search Usage
- Check logs for repeated failures
- Adjust rate limiting if needed
- Consider using mock mode for development

### 4. Agent Instructions
Update your agent instructions to handle search limitations:
```python
instructions="""
You are a research agent.
- Use web search to find current information
- If search is unavailable, use your knowledge base
- Always note when information may not be current
- Provide citations when search works
"""
```

## 📈 Performance Comparison

| Mode | Speed | Reliability | Network Required | Best For |
|------|--------|-------------|------------------|----------|
| Robust | Medium | High ✅ | Yes | Production |
| Mock | Fast | Perfect ✅ | No | Testing |
| Original | Fast | Low ❌ | Yes | Stable networks only |

## 🆘 Troubleshooting

### Still Getting Errors?
1. **Check Rate Limits**: Increase `SEARCH_MIN_INTERVAL`
2. **Increase Retries**: Set `SEARCH_MAX_RETRIES=5`
3. **Use Mock Mode**: Test without network dependency
4. **Check Network**: Verify internet connectivity

### Debug Mode
Enable logging to see what's happening:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Agent Not Using Search?
- Verify agent has search tools configured
- Check agent instructions mention web search
- Look for fallback responses in output

## 💡 Alternative Approaches

### 1. Cached Search Results
Store successful search results to reduce API calls:
```python
# Implement caching in robust_search_tools.py
# (Future enhancement)
```

### 2. Multiple Search Providers
Add support for other search APIs:
- Bing Search API
- Google Custom Search
- SerpAPI
- (Requires API keys)

### 3. Pre-loaded Knowledge
For critical topics, pre-load information into agent knowledge:
```python
instructions="""
Key facts about AI and jobs (as of 2024):
- WEF projects 69M new jobs, 83M displaced by 2027
- McKinsey emphasizes need for reskilling
- [Add other key facts here]

Use web search to supplement this information.
"""
```

## 📝 Summary

The improved search system provides:
- ✅ **Reliability**: Handles rate limits and network issues
- ✅ **Flexibility**: Multiple modes for different needs  
- ✅ **Debugging**: Logging and error reporting
- ✅ **Testing**: Mock mode for development
- ✅ **Configuration**: Environment variable control

Your multi-agent systems will now work consistently even when DuckDuckGo search has issues!

---

*For questions or issues, check the logs and consider using mock mode for testing your multi-agent workflows.*