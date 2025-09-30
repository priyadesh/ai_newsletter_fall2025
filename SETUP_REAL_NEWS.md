# 🚀 Setting Up Real News Sources

This guide will help you configure the AI News Newsletter to use real news sources instead of mock data.

## 📋 Prerequisites

You'll need API keys from one or more of these services:

### Required: OpenAI API Key
- **Purpose**: AI processing for summarization and editorial generation
- **Get it**: https://platform.openai.com/api-keys
- **Cost**: Pay-per-use (typically $0.01-0.10 per newsletter)

### Recommended: SerpAPI Key
- **Purpose**: Google News search for latest articles
- **Get it**: https://serpapi.com/
- **Free tier**: 100 searches/month
- **Cost**: $50/month for 5,000 searches

### Alternative: NewsAPI Key
- **Purpose**: Alternative news source
- **Get it**: https://newsapi.org/
- **Free tier**: 1,000 requests/day
- **Cost**: Free for development

## 🔧 Quick Setup

### Option 1: Interactive Setup (Recommended)
```bash
python setup_api_keys.py
```

This script will guide you through entering your API keys interactively.

### Option 2: Manual Setup
Edit the `.env` file and replace the placeholder values:

```bash
# Required
OPENAI_API_KEY=sk-your-actual-openai-key-here

# Recommended (choose one or both)
SERPAPI_API_KEY=your-serpapi-key-here
NEWSAPI_API_KEY=your-newsapi-key-here
```

## 🚀 Starting with Real News

1. **Configure your API keys** using one of the methods above
2. **Restart the server**:
   ```bash
   # Stop current server (Ctrl+C)
   uv run python main.py
   ```
3. **Check system status**: Visit http://localhost:8080/api/v1/health
4. **View your newsletter**: Visit http://localhost:8080

## 📊 System Status

The health check endpoint will show you:
- Which API keys are configured
- Whether you're in demo mode or production mode
- Available news sources

### Demo Mode vs Production Mode

- **Demo Mode**: Uses mock data (no real API keys)
- **Production Mode**: Uses real news sources and AI processing

## 🔍 Troubleshooting

### "No news sources configured"
- Add at least one news API key (SerpAPI or NewsAPI)
- Restart the server after adding keys

### "OpenAI API key missing"
- Add your OpenAI API key to `.env`
- Ensure the key starts with `sk-`

### "Rate limit exceeded"
- Check your API usage limits
- Consider upgrading your API plan
- The system will fall back to mock data if APIs fail

### "Connection errors"
- Check your internet connection
- Verify API keys are correct
- Check API service status pages

## 💡 Tips

1. **Start with SerpAPI**: It provides the most comprehensive news coverage
2. **Monitor usage**: Check your API usage regularly to avoid overages
3. **Fallback behavior**: The system gracefully falls back to mock data if APIs fail
4. **Caching**: News is cached for 10 minutes to reduce API calls

## 🆘 Need Help?

- Check the health endpoint: http://localhost:8080/api/v1/health
- View API documentation: http://localhost:8080/docs
- Check server logs for detailed error messages

## 📈 Expected Costs

For a newsletter generated once per day:
- **OpenAI**: ~$0.01-0.05 per newsletter
- **SerpAPI**: ~$0.10-0.50 per newsletter (depending on plan)
- **NewsAPI**: Free (within limits)

Total: ~$0.11-0.55 per newsletter
