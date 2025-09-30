# =============================================================================
#  Filename: ai_service.py
#
#  Short Description: AI service for article summarization and editorial generation
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

import os
import logging
from typing import List, Optional
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

from ..models.news_models import NewsArticle, NewsSummary, EditorialArticle, NewsletterData
from ..config import settings

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered content generation and processing."""
    
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        
        if settings.has_openai_key:
            self.llm = ChatOpenAI(
                model="gpt-4o", 
                temperature=0.7, 
                openai_api_key=self.openai_api_key
            )
            logger.info("AI Service initialized with OpenAI GPT-4o")
        else:
            self.llm = None
            logger.warning("AI Service initialized in mock mode - no OpenAI API key")
    
    async def summarize_article(self, article: NewsArticle) -> NewsSummary:
        """Summarize an article using AI or mock data."""
        if self.llm and not settings.is_demo_mode:
            return self._ai_summarize_article(article)
        else:
            return self._mock_summarize_article(article)
    
    async def write_editorial(self, summaries: List[NewsSummary]) -> EditorialArticle:
        """Write editorial content using AI or mock data."""
        if self.llm and not settings.is_demo_mode:
            return self._ai_write_editorial(summaries)
        else:
            return self._mock_write_editorial(summaries)
    
    def _ai_summarize_article(self, article: NewsArticle) -> NewsSummary:
        """Use AI to summarize an article."""
        try:
            # Create Editor Agent
            editor_agent = Agent(
                role='News Editor',
                goal='Create engaging, accurate summaries of AI news articles',
                backstory='You are an experienced tech journalist who specializes in making complex AI topics accessible to general audiences.',
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            )
            
            # Create summarization task
            summary_task = Task(
                description=f"""
                Summarize this AI news article in 2-3 sentences:
                
                Title: {article.title}
                Source: {article.source}
                Content: {article.snippet}
                
                Create:
                1. A catchy, engaging title (different from original)
                2. A clear 2-3 sentence summary
                3. 3-5 key points
                4. A relevance score (0.0-1.0) for AI/tech audience
                
                Format your response as:
                TITLE: [catchy title]
                SUMMARY: [2-3 sentence summary]
                KEY_POINTS: [bullet point 1, bullet point 2, bullet point 3]
                RELEVANCE: [score between 0.0 and 1.0]
                """,
                agent=editor_agent,
                expected_output="A structured summary with TITLE, SUMMARY, KEY_POINTS, and RELEVANCE sections"
            )
            
            # Execute task
            crew = Crew(
                agents=[editor_agent],
                tasks=[summary_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Parse the result
            return self._parse_summary_result(result, article)
            
        except Exception as e:
            logger.error(f"AI summarization failed: {e}")
            return self._mock_summarize_article(article)
    
    def _ai_write_editorial(self, summaries: List[NewsSummary]) -> EditorialArticle:
        """Use AI to write editorial content."""
        try:
            # Create Senior Editor Agent
            senior_editor = Agent(
                role='Senior Editor',
                goal='Write compelling editorial narratives that connect AI trends',
                backstory='You are a senior tech editor with deep expertise in AI trends and the ability to weave compelling narratives from multiple news stories.',
                verbose=True,
                allow_delegation=False,
                llm=self.llm
            )
            
            # Prepare summary context
            summary_context = "\n".join([
                f"- {summary.catchy_title}: {summary.summary}"
                for summary in summaries[:5]  # Use top 5 summaries
            ])
            
            # Create editorial task
            editorial_task = Task(
                description=f"""
                Write a compelling 200-300 word editorial article that introduces an AI newsletter and weaves together themes from these news stories:
                
                {summary_context}
                
                Requirements:
                1. Engaging title that captures current AI trends
                2. 200-300 words of compelling narrative
                3. Connect the stories to broader AI themes
                4. Professional but accessible tone
                5. End with forward-looking perspective
                
                Format your response as:
                TITLE: [editorial title]
                CONTENT: [200-300 word editorial content]
                THEME: [main theme/topic]
                AUTHOR: [editorial author name]
                """,
                agent=senior_editor,
                expected_output="A structured editorial with TITLE, CONTENT, THEME, and AUTHOR sections"
            )
            
            # Execute task
            crew = Crew(
                agents=[senior_editor],
                tasks=[editorial_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            # Parse the result
            return self._parse_editorial_result(result)
            
        except Exception as e:
            logger.error(f"AI editorial generation failed: {e}")
            return self._mock_write_editorial(summaries)
    
    def _parse_summary_result(self, result: str, article: NewsArticle) -> NewsSummary:
        """Parse AI result into NewsSummary object."""
        try:
            lines = str(result).split('\n')
            title = ""
            summary = ""
            key_points = []
            relevance = 0.8
            
            for line in lines:
                if line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()
                elif line.startswith('SUMMARY:'):
                    summary = line.replace('SUMMARY:', '').strip()
                elif line.startswith('KEY_POINTS:'):
                    points_text = line.replace('KEY_POINTS:', '').strip()
                    key_points = [p.strip() for p in points_text.split(',') if p.strip()]
                elif line.startswith('RELEVANCE:'):
                    try:
                        relevance = float(line.replace('RELEVANCE:', '').strip())
                    except ValueError:
                        relevance = 0.8
            
            # If no key points were parsed, generate generic ones from the title
            if not key_points:
                key_points = [
                    f"Key development in {article.source}",
                    f"Related to: {article.title[:80]}",
                    "Significant impact on AI industry"
                ]
            
            return NewsSummary(
                id=f"summary_{abs(hash(article.title + str(article.url))) % 100000:05d}",
                catchy_title=title or article.title,
                summary=summary or article.snippet,
                key_points=key_points,
                relevance_score=relevance,
                original_article=article
            )
            
        except Exception as e:
            logger.error(f"Failed to parse summary result: {e}")
            return self._mock_summarize_article(article)
    
    def _parse_editorial_result(self, result: str) -> EditorialArticle:
        """Parse AI result into EditorialArticle object."""
        try:
            lines = str(result).split('\n')
            title = ""
            content = ""
            theme = "AI Innovation"
            author = "AI Newsletter Editor"
            
            for line in lines:
                if line.startswith('TITLE:'):
                    title = line.replace('TITLE:', '').strip()
                elif line.startswith('CONTENT:'):
                    content = line.replace('CONTENT:', '').strip()
                elif line.startswith('THEME:'):
                    theme = line.replace('THEME:', '').strip()
                # Ignore AUTHOR: from AI output - we'll use our own
            
            return EditorialArticle(
                title=title or "The AI Revolution: Where We Stand Today",
                content=content or "AI continues to reshape our world...",
                theme=theme,
                author="Senior Editor"  # Always use "Senior Editor" as requested
            )
            
        except Exception as e:
            logger.error(f"Failed to parse editorial result: {e}")
            return self._mock_write_editorial([])
    
    def _mock_summarize_article(self, article: NewsArticle) -> NewsSummary:
        """Generate mock summary for testing."""
        catchy_titles = [
            f"Breaking: {article.title}",
            f"🚀 {article.title}",
            f"Revolutionary: {article.title}",
            f"Game-Changer: {article.title}",
            f"Next-Gen: {article.title}"
        ]
        
        import random
        catchy_title = random.choice(catchy_titles)
        
        return NewsSummary(
            id=f"summary_{abs(hash(article.title + str(article.url))) % 100000:05d}",
            catchy_title=catchy_title,
            summary=f"{article.snippet} This development represents a significant step forward in AI technology.",
            key_points=[
                "Significant advancement in AI capabilities",
                "Potential impact on various industries", 
                "Continued innovation in the field"
            ],
            relevance_score=random.uniform(0.7, 0.95),
            original_article=article
        )
    
    def _mock_write_editorial(self, summaries: List[NewsSummary]) -> EditorialArticle:
        """Generate mock editorial for testing."""
        return EditorialArticle(
            title="The AI Revolution: Where We Stand Today",
            content="""The artificial intelligence landscape continues to evolve at an unprecedented pace, with each passing day bringing new breakthroughs that reshape our understanding of what's possible. From language models that can engage in sophisticated reasoning to autonomous systems that navigate complex environments, we're witnessing a technological renaissance that promises to transform every aspect of human life.

Today's headlines reflect this rapid advancement, showcasing innovations that span from fundamental research to practical applications. These developments aren't just technical achievements—they represent humanity's collective effort to push the boundaries of intelligence itself. As we stand at this inflection point, it's clear that the future belongs to those who can harness the power of AI responsibly and creatively.

The journey ahead promises even greater discoveries, but it also demands thoughtful consideration of the ethical implications and societal impacts of these powerful technologies.""",
            theme="AI Innovation and Future Trends",
            author="Senior Editor"
        )
