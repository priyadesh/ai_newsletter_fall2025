#!/usr/bin/env python3
# =============================================================================
#  Filename: setup_api_keys.py
#
#  Short Description: Interactive script to set up API keys for real news
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import os
import sys
from pathlib import Path

def main():
    print("🔑 AI News Newsletter - API Key Setup")
    print("=" * 50)
    print()
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found. Please run this script from the project root.")
        sys.exit(1)
    
    print("📝 Setting up API keys for real news sources...")
    print()
    
    # Read current .env content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Get OpenAI API key
    print("🤖 OpenAI API Key (Required for AI processing)")
    print("   Get your key from: https://platform.openai.com/api-keys")
    openai_key = input("   Enter your OpenAI API key: ").strip()
    
    if not openai_key:
        print("⚠️  OpenAI API key is required for AI processing!")
        return
    
    # Get SerpAPI key
    print("\n🔍 SerpAPI Key (Recommended for news search)")
    print("   Get your key from: https://serpapi.com/")
    print("   Free tier: 100 searches/month")
    serpapi_key = input("   Enter your SerpAPI key (or press Enter to skip): ").strip()
    
    # Get NewsAPI key
    print("\n📰 NewsAPI Key (Alternative news source)")
    print("   Get your key from: https://newsapi.org/")
    print("   Free tier: 1000 requests/day")
    newsapi_key = input("   Enter your NewsAPI key (or press Enter to skip): ").strip()
    
    # Update .env content
    lines = content.split('\n')
    updated_lines = []
    
    for line in lines:
        if line.startswith('OPENAI_API_KEY='):
            updated_lines.append(f'OPENAI_API_KEY={openai_key}')
        elif line.startswith('SERPAPI_API_KEY='):
            updated_lines.append(f'SERPAPI_API_KEY={serpapi_key}')
        elif line.startswith('NEWSAPI_API_KEY='):
            updated_lines.append(f'NEWSAPI_API_KEY={newsapi_key}')
        else:
            updated_lines.append(line)
    
    # Write updated .env
    with open(env_file, 'w') as f:
        f.write('\n'.join(updated_lines))
    
    print("\n✅ API keys saved to .env file!")
    print()
    
    # Show configuration summary
    print("📊 Configuration Summary:")
    print(f"   OpenAI API: {'✅ Configured' if openai_key else '❌ Missing'}")
    print(f"   SerpAPI: {'✅ Configured' if serpapi_key else '❌ Missing'}")
    print(f"   NewsAPI: {'✅ Configured' if newsapi_key else '❌ Missing'}")
    print()
    
    if openai_key and (serpapi_key or newsapi_key):
        print("🎉 Perfect! You're ready for real news!")
        print("   Restart the server to use your new configuration.")
    elif openai_key:
        print("⚠️  You have OpenAI configured but no news sources.")
        print("   The system will use mock news data.")
    else:
        print("❌ OpenAI API key is required for AI processing.")
    
    print("\n🚀 Next steps:")
    print("   1. Restart the server: Ctrl+C then run 'uv run python main.py'")
    print("   2. Visit http://localhost:8080 to see your newsletter")
    print("   3. Check http://localhost:8080/api/v1/health for system status")

if __name__ == "__main__":
    main()
