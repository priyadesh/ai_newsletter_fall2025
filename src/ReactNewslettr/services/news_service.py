# =============================================================================
#  Filename: news_service.py
#
#  Short Description: Service for fetching news articles from various sources
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import os
import requests
from typing import List, Optional
from ..models.news_models import NewsArticle
from ..config import settings
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        self.serpapi_api_key = settings.serpapi_api_key
        self.newsapi_api_key = settings.newsapi_api_key
        
        if not settings.has_any_news_source:
            logger.warning("No news API keys found. Using mock news data.")

    async def fetch_articles(self, query: str = settings.news_query, num_articles: int = settings.max_articles) -> List[NewsArticle]:
        """Fetch articles from configured news sources."""
        if settings.is_demo_mode:
            return self._get_mock_articles(num_articles)

        articles = []
        if settings.has_serpapi_key:
            logger.info("Attempting to fetch news using SerpAPI...")
            articles = self._fetch_from_serpapi(query, num_articles)
            if articles:
                logger.info(f"Successfully fetched {len(articles)} articles from SerpAPI.")
                return articles
            else:
                logger.warning("SerpAPI returned no articles or failed. Falling back to NewsAPI if configured.")

        if settings.has_newsapi_key:
            logger.info("Attempting to fetch news using NewsAPI...")
            articles = self._fetch_from_newsapi(query, num_articles)
            if articles:
                logger.info(f"Successfully fetched {len(articles)} articles from NewsAPI.")
                return articles
            else:
                logger.warning("NewsAPI returned no articles or failed. Falling back to mock data.")

        logger.warning("All news sources failed or not configured. Using mock news data.")
        return self._get_mock_articles(num_articles)

    def _fetch_from_serpapi(self, query: str, num_articles: int) -> List[NewsArticle]:
        """Fetch articles from SerpAPI."""
        try:
            # Import serpapi here to avoid import errors if not installed
            from serpapi import Client
            
            client = Client(api_key=self.serpapi_api_key)
            results = client.search({
                "engine": "google",
                "q": query,
                "tbm": "nws",
                "num": num_articles
            })
            
            news_results = results.get("news_results", [])
            logger.info(f"SerpAPI returned {len(news_results)} news results")
            
            articles = []
            for item in news_results:
                if item.get("link") and item.get("title") and item.get("snippet"):
                    # Handle published_date - SerpAPI often returns relative times like "9 hours ago"
                    # which can't be parsed as datetime, so we skip it
                    pub_date = None
                    if item.get("date"):
                        try:
                            # Try to parse as datetime if it's a proper date string
                            from dateutil import parser
                            pub_date = parser.parse(item["date"])
                        except:
                            # If parsing fails (e.g., "9 hours ago"), just use None
                            pub_date = None
                    
                    articles.append(NewsArticle(
                        title=item["title"],
                        url=item["link"],
                        snippet=item["snippet"],
                        thumbnail=item.get("thumbnail"),
                        source=item.get("source", {}).get("name") if isinstance(item.get("source"), dict) else item.get("source"),
                        published_date=pub_date
                    ))
            
            logger.info(f"Parsed {len(articles)} valid articles from SerpAPI")
            return articles
        except ImportError:
            logger.warning("SerpAPI package not installed. Skipping SerpAPI fetch.")
            return []
        except Exception as e:
            logger.error(f"Error fetching news from SerpAPI: {e}", exc_info=True)
            return []

    def _fetch_from_newsapi(self, query: str, num_articles: int) -> List[NewsArticle]:
        """Fetch articles from NewsAPI."""
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "pageSize": num_articles,
                "apiKey": self.newsapi_api_key,
                "language": "en",
                "sortBy": "publishedAt"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            articles = []
            for item in data.get("articles", []):
                if item.get("url") and item.get("title") and item.get("description"):
                    articles.append(NewsArticle(
                        title=item["title"],
                        url=item["url"],
                        snippet=item["description"],
                        full_text=item.get("content"),
                        thumbnail=item.get("urlToImage"),
                        source=item.get("source", {}).get("name"),
                        published_date=item.get("publishedAt")
                    ))
            return articles
        except Exception as e:
            logger.error(f"Error fetching news from NewsAPI: {e}")
            return []

    def _get_mock_articles(self, num_articles: int) -> List[NewsArticle]:
        """Generate mock articles for testing."""
        mock_articles_data = [
            {
                "title": "GPT-5 Unveiled: OpenAI's Next-Gen AI Promises Unprecedented Capabilities",
                "url": "https://openai.com/blog/gpt-5-announcement",
                "snippet": "OpenAI officially announced GPT-5, highlighting its advanced reasoning, multimodal understanding, and improved efficiency. Experts predict a new era for AI applications.",
                "full_text": "The highly anticipated GPT-5 model from OpenAI is set to redefine artificial intelligence. With significant advancements in natural language processing, computer vision, and complex problem-solving, GPT-5 is expected to power a new generation of AI tools and services. Early benchmarks suggest a leap in performance over its predecessors, particularly in areas requiring deep contextual understanding and creative generation. Developers are eager to explore its potential in various industries, from healthcare to entertainment.",
                "thumbnail": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop&crop=center",
                "source": "OpenAI Blog",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "Google DeepMind Achieves Breakthrough in AI for Scientific Discovery",
                "url": "https://blog.google/technology/ai/deepmind-scientific-discovery",
                "snippet": "DeepMind's latest AI model demonstrates remarkable ability to accelerate scientific research, predicting complex molecular structures and optimizing experimental designs.",
                "full_text": "Researchers at Google DeepMind have published groundbreaking results on an AI system designed to aid scientific discovery. The AI, trained on vast datasets of scientific literature and experimental data, can hypothesize new materials, predict protein folding with unprecedented accuracy, and even suggest novel chemical synthesis pathways. This development is expected to significantly reduce the time and cost associated with fundamental research, opening doors to solutions for global challenges in medicine, energy, and environmental science.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685100-26b1d0437b0c?w=400&h=250&fit=crop&crop=center",
                "source": "Google AI Blog",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "AI Ethics in Focus: New Regulations Proposed for Responsible AI Development",
                "url": "https://www.techpolicy.gov/ai-ethics-regulations",
                "snippet": "Governments worldwide are collaborating on new ethical guidelines and regulations to ensure AI development remains human-centric and prevents misuse.",
                "full_text": "The rapid advancement of AI has prompted a global discussion on ethical considerations. A consortium of international bodies and governments has proposed a new framework for AI regulation, focusing on transparency, accountability, fairness, and privacy. The proposed laws aim to balance innovation with the need to protect societal values and prevent the deployment of harmful AI systems. Public consultations are underway, with strong calls for robust oversight and independent auditing of AI algorithms.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685077-07904173c801?w=400&h=250&fit=crop&crop=center",
                "source": "TechPolicy.gov",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "The Rise of AI Companions: More Than Just Chatbots",
                "url": "https://www.futuretech.com/ai-companions-evolution",
                "snippet": "AI companions are evolving beyond simple chatbots, offering personalized assistance, emotional support, and even creative collaboration.",
                "full_text": "The next frontier in personal AI is the development of sophisticated AI companions. These systems, equipped with advanced emotional intelligence and learning capabilities, are designed to integrate seamlessly into daily life, providing proactive assistance, engaging in meaningful conversations, and adapting to individual user preferences. Companies are investing heavily in this sector, envisioning a future where AI companions become indispensable partners for productivity, well-being, and companionship.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685090-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "Future Tech Magazine",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "AI in Healthcare: Revolutionizing Diagnostics and Drug Discovery",
                "url": "https://www.medtechdaily.com/ai-healthcare-revolution",
                "snippet": "AI-powered tools are transforming healthcare, enabling earlier disease detection, more accurate diagnoses, and accelerating the development of new therapies.",
                "full_text": "Artificial intelligence is rapidly becoming a cornerstone of modern healthcare. From analyzing medical images to identify subtle signs of disease to sifting through vast genomic data for drug targets, AI is enhancing every aspect of patient care and biomedical research. Startups and established pharmaceutical companies are leveraging AI to streamline clinical trials, personalize treatment plans, and discover novel compounds, promising a future of more effective and accessible healthcare.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685082-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "MedTech Daily",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "Quantum Computing Meets AI: A New Frontier for Complex Problem Solving",
                "url": "https://www.quantumaijournal.com/hybrid-systems",
                "snippet": "The convergence of quantum computing and AI is paving the way for hybrid systems capable of tackling problems currently beyond classical computation.",
                "full_text": "The synergy between quantum computing and artificial intelligence is creating exciting new possibilities. Researchers are developing 'quantum AI' algorithms that leverage the unique properties of quantum mechanics to process information in ways classical computers cannot. This could lead to breakthroughs in fields like cryptography, materials science, and drug development, solving problems that are intractable even for today's most powerful supercomputers. The first practical applications of these hybrid systems are eagerly awaited.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685072-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "Quantum AI Journal",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "AI in Education: Personalized Learning and Administrative Efficiency",
                "url": "https://www.edutechinsights.com/ai-in-education",
                "snippet": "AI is being integrated into educational systems to offer personalized learning experiences, automate administrative tasks, and provide intelligent tutoring.",
                "full_text": "Educational institutions are increasingly adopting AI to enhance learning outcomes and operational efficiency. AI-powered platforms can adapt curricula to individual student needs, provide instant feedback, and identify areas where students might struggle. Beyond the classroom, AI is automating grading, scheduling, and resource allocation, freeing up educators to focus more on teaching and mentorship. The goal is to create a more engaging, effective, and equitable learning environment for all.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685067-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "EduTech Insights",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "The Future of Work: How AI is Reshaping Industries and Job Markets",
                "url": "https://www.globalworkforce.org/ai-future-of-work",
                "snippet": "AI is fundamentally altering the landscape of work, creating new job roles while automating others, necessitating a focus on reskilling and adaptation.",
                "full_text": "The integration of AI into various industries is leading to a significant transformation of the global job market. While some routine tasks are being automated, new roles requiring AI-specific skills, creativity, and critical thinking are emerging. Governments and corporations are investing in reskilling initiatives to prepare the workforce for these changes. The future of work will likely involve a collaborative human-AI ecosystem, where human ingenuity is augmented by artificial intelligence.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685057-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "Global Workforce Org",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "AI in Creative Arts: Generating Music, Art, and Literature",
                "url": "https://www.creativeai.art/generative-models",
                "snippet": "Generative AI models are pushing the boundaries of creativity, producing original music compositions, visual art, and even compelling literary works.",
                "full_text": "Artificial intelligence is no longer just for logic and data; it's now a powerful tool in the creative arts. AI algorithms are being used to compose symphonies, paint digital masterpieces, and write poetry and prose that can be indistinguishable from human-created works. This raises fascinating questions about authorship, originality, and the very definition of creativity. Artists are increasingly collaborating with AI, using it as a muse and a tool to explore new artistic frontiers.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685047-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "Creative AI Hub",
                "published_date": datetime.now().isoformat()
            },
            {
                "title": "Edge AI: Bringing Intelligence Closer to the Source",
                "url": "https://www.edgecomputingtimes.com/ai-on-device",
                "snippet": "The trend of deploying AI models directly on devices (edge AI) is enhancing privacy, reducing latency, and enabling new applications in IoT and robotics.",
                "full_text": "Edge AI, the practice of running AI algorithms directly on local devices rather than in the cloud, is gaining significant traction. This approach offers numerous benefits, including enhanced data privacy, reduced latency, and lower bandwidth requirements. It's particularly crucial for applications in autonomous vehicles, smart home devices, and industrial IoT, where real-time processing and offline capabilities are essential. The development of specialized AI chips is accelerating this shift towards ubiquitous, on-device intelligence.",
                "thumbnail": "https://images.unsplash.com/photo-1696258685037-d03775862167?w=400&h=250&fit=crop&crop=center",
                "source": "Edge Computing Times",
                "published_date": datetime.now().isoformat()
            }
        ]
        
        # Assign unique IDs and ensure enough articles
        articles = []
        for i in range(num_articles):
            article_data = mock_articles_data[i % len(mock_articles_data)]
            articles.append(NewsArticle(**article_data))
        
        return articles
