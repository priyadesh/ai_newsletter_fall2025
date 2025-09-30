# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. WebSocket Connection Errors (403 Forbidden)

**Problem**: Getting WebSocket connection errors like:
```
INFO: connection rejected (403 Forbidden)
INFO: connection closed
```

**Solution**:
1. **Kill existing processes**:
   ```bash
   # Find processes using port 8080
   lsof -i :8080
   
   # Kill conflicting processes
   kill -9 <PID>
   ```

2. **Check for conflicting services**:
   ```bash
   # Check for NiceGUI or other services
   ps aux | grep -i nicegui
   ps aux | grep python
   ```

3. **Restart cleanly**:
   ```bash
   # Stop all processes
   pkill -f "python main.py"
   
   # Start fresh
   uv run python main.py
   ```

### 2. API Key Issues

**Problem**: OpenAI API errors or missing API keys

**Solution**:
1. **Check .env file**:
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

2. **Use mock data mode**:
   - The system automatically falls back to mock data when API keys are missing
   - Set `OPENAI_API_KEY=sk-test-key-placeholder` for testing

3. **Get real API key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key
   - Update `.env` file with real key

### 3. Port Already in Use

**Problem**: `Address already in use` error

**Solution**:
1. **Find process using port**:
   ```bash
   lsof -i :8080
   ```

2. **Kill the process**:
   ```bash
   kill -9 <PID>
   ```

3. **Or use different port**:
   ```bash
   # Update .env file
   PORT=8081
   ```

### 4. Import Errors

**Problem**: Module import errors

**Solution**:
1. **Reinstall dependencies**:
   ```bash
   uv sync --reinstall
   ```

2. **Check Python path**:
   ```bash
   uv run python -c "import sys; print(sys.path)"
   ```

### 5. Cache Issues

**Problem**: Stale or corrupted cache

**Solution**:
1. **Clear cache via API**:
   ```bash
   curl -X DELETE http://localhost:8080/api/v1/cache
   ```

2. **Restart server**:
   ```bash
   # Cache is automatically cleared on restart
   ```

## 🚀 Quick Start (Clean Installation)

1. **Kill all existing processes**:
   ```bash
   pkill -f python
   ```

2. **Clean install**:
   ```bash
   uv sync
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start server**:
   ```bash
   uv run python main.py
   ```

5. **Test endpoints**:
   ```bash
   # Health check
   curl http://localhost:8080/api/v1/health
   
   # Newsletter
   curl http://localhost:8080/api/v1/newsletter
   
   # Main page
   curl http://localhost:8080/
   ```

## 🔍 Debugging Tips

### Enable Debug Mode
```bash
# In .env file
DEBUG=True
```

### Check Logs
```bash
# Server logs will show in terminal
# Look for error messages and stack traces
```

### Test Individual Components
```bash
# Run tests
uv run python -m pytest tests/ -v

# Run demo
uv run python demo.py
```

### API Testing
```bash
# Test all endpoints
curl http://localhost:8080/api/v1/health
curl http://localhost:8080/api/v1/newsletter
curl http://localhost:8080/api/v1/cache/status
```

## 📞 Getting Help

1. **Check server logs** for error messages
2. **Verify API keys** are correctly set
3. **Test with mock data** first (no API keys needed)
4. **Check port availability** (8080)
5. **Restart cleanly** if issues persist

## ✅ Success Indicators

- Health check returns `{"status":"healthy"}`
- Newsletter endpoint returns `{"success":true}`
- Main page loads HTML content
- No WebSocket connection errors in logs
- Server starts without import errors
