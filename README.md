# 🤖 AI News Newsletter

A multi-agent AI system that collects the latest AI-related news, summarizes it, verifies accuracy, and produces a creative editorial newsletter with a React frontend and FastAPI backend.

## ✨ Features

- **Multi-Agent Workflow**: Three specialized AI agents working together
  - **Reporter Agent**: Fetches latest AI news from SerpAPI
  - **Editor Agent**: Creates engaging summaries and catchy titles
  - **Senior Editor Agent**: Reviews content and writes editorial narratives
- **Modern Web Interface**: Beautiful React-based frontend with Tailwind CSS
- **FastAPI Backend**: High-performance API with automatic documentation
- **Intelligent Caching**: TTL-based caching for optimal performance
- **Responsive Design**: Works perfectly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key
- (Optional) SerpAPI key for real news data

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd react-newsletter
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Open your browser**:
   - Main app: http://localhost:8080
   - API docs: http://localhost:8080/docs

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `SERPAPI_API_KEY` | SerpAPI key for news (optional) | - |
| `HOST` | Server host | localhost |
| `PORT` | Server port | 8080 |
| `CACHE_TTL_MINUTES` | Cache duration | 10 |
| `MAX_ARTICLES` | Number of articles to fetch | 10 |

### API Keys Setup

1. **OpenAI API Key** (Required):
   - Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Add to `.env` file

2. **SerpAPI Key** (Optional):
   - Get your key from [SerpAPI](https://serpapi.com/)
   - If not provided, the system will use mock data

## ��️ Architecture

### Multi-Agent System

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Reporter Agent │───▶│   Editor Agent  │───▶│Senior Editor Agent│
│                 │    │                 │    │                 │
│ • Fetch news    │    │ • Summarize     │    │ • Review & polish│
│ • Validate      │    │ • Create titles │    │ • Write editorial│
│ • Enhance data  │    │ • Extract points│    │ • Quality check │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Tech Stack

- **Backend**: FastAPI + Python 3.12
- **Frontend**: React + Tailwind CSS
- **AI**: OpenAI GPT-4
- **Caching**: TTLCache
- **News**: SerpAPI (with mock fallback)

## 📡 API Endpoints

### Core Endpoints

- `GET /` - Main newsletter interface
- `GET /article/{id}` - Individual article page
- `GET /api/v1/newsletter` - Newsletter data (JSON)
- `GET /api/v1/newsletter/{id}` - Specific article (JSON)
- `GET /api/v1/health` - Health check

### Cache Management

- `GET /api/v1/cache/status` - Cache statistics
- `DELETE /api/v1/cache` - Clear cache

## 🎨 UI Features

### Landing Page
- **Editorial Section**: AI-generated narrative about current trends
- **News Grid**: 10 latest articles with thumbnails
- **Responsive Design**: Adapts to all screen sizes
- **Real-time Updates**: Refresh button with loading states

### Article Page
- **Full Article View**: Detailed summary and key points
- **Source Links**: Direct links to original articles
- **Share Functionality**: Built-in sharing capabilities
- **Relevance Scoring**: AI-calculated relevance scores

## 🔄 Workflow

1. **Reporter Agent** fetches 10 latest AI news articles
2. **Editor Agent** processes each article:
   - Creates catchy titles
   - Writes 2-3 sentence summaries
   - Extracts key points
   - Calculates relevance scores
3. **Senior Editor Agent**:
   - Reviews and polishes summaries
   - Writes 200-300 word editorial
   - Ensures quality and accuracy
4. **Backend** caches results for 10 minutes
5. **Frontend** displays beautiful newsletter interface

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Lint code
ruff check .

# Format code
ruff format .
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production
```bash
uvicorn src.ReactNewslettr.api.main:app --host 0.0.0.0 --port 8080
```

### Docker (Optional)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
EXPOSE 8080
CMD ["python", "main.py"]
```

## 📊 Performance

- **Caching**: 10-minute TTL reduces API calls
- **Async Processing**: Non-blocking I/O operations
- **Error Handling**: Graceful fallbacks and retry logic
- **Mock Data**: Works without external APIs for testing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is part of the SupportVectors AI Lab training material.

## 🆘 Support

- **Documentation**: Check `/docs` endpoint
- **Health Check**: Visit `/api/v1/health`
- **Issues**: Create GitHub issues for bugs

---

**Built with ❤️ for the AI community**
