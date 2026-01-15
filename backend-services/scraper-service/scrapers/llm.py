"""
LLM-powered universal scraper using ScrapingBee + Claude
Works with any e-commerce site
"""
from typing import Dict, Any
from datetime import datetime
import httpx
import json
import logging
from bs4 import BeautifulSoup
from fastapi import HTTPException, status

from models import Review, ProductMetadata, ScrapeResponse
from config import settings

logger = logging.getLogger(__name__)


class UniversalLLMScraper:
    """AI-powered scraper using ScrapingBee + Claude for any e-commerce site"""
    
    def __init__(self):
        self.scrapingbee_url = settings.SCRAPINGBEE_URL
        
    async def scrape(self, url: str, max_reviews: int, platform: str) -> ScrapeResponse:
        """Scrape any e-commerce site using AI"""
        start_time = datetime.utcnow()
        logger.info(f"[LLM] Scraping {platform}: {url}")
        
        try:
            # Step 1: Fetch HTML with ScrapingBee
            html_content = await self._fetch_with_scrapingbee(url)
            
            # Step 2: Extract data using Claude
            extracted_data = await self._extract_with_llm(html_content, platform, max_reviews)
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            return ScrapeResponse(
                success=True,
                platform=platform,
                scraping_method="llm",
                product_metadata=extracted_data["metadata"],
                reviews=extracted_data["reviews"],
                total_reviews_scraped=len(extracted_data["reviews"]),
                sampling_strategy="llm_intelligent",
                processing_time_seconds=round(processing_time, 2),
                timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logger.error(f"LLM scraping failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"LLM scraping failed: {str(e)}"
            )
    
    async def _fetch_with_scrapingbee(self, url: str) -> str:
        """Fetch page HTML using ScrapingBee"""
        if not settings.is_scrapingbee_configured:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="ScrapingBee API key not configured. Set SCRAPINGBEE_API_KEY environment variable."
            )
        
        params = {
            'api_key': settings.SCRAPINGBEE_API_KEY,
            'url': url,
            'render_js': str(settings.SCRAPINGBEE_RENDER_JS).lower(),
            'premium_proxy': str(settings.SCRAPINGBEE_PREMIUM_PROXY).lower(),
            'country_code': settings.SCRAPINGBEE_COUNTRY_CODE
        }
        
        async with httpx.AsyncClient(timeout=settings.SCRAPINGBEE_TIMEOUT) as client:
            response = await client.get(self.scrapingbee_url, params=params)
            
            if response.status_code != 200:
                raise Exception(f"ScrapingBee failed: {response.status_code} - {response.text}")
            
            logger.info("Successfully fetched HTML via ScrapingBee")
            return response.text
    
    async def _extract_with_llm(self, html: str, platform: str, max_reviews: int) -> Dict[str, Any]:
        """Extract structured data using Claude API"""
        if not settings.is_anthropic_configured:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Anthropic API key not configured. Set ANTHROPIC_API_KEY environment variable."
            )
        
        # Clean and truncate HTML
        clean_html = self._clean_html(html)
        
        # Build extraction prompt
        prompt = self._build_extraction_prompt(clean_html, platform, max_reviews)
        
        # Call Claude API
        extracted_json = await self._call_claude_api(prompt)
        
        # Parse and validate response
        return self._parse_llm_response(extracted_json)
    
    def _clean_html(self, html: str) -> str:
        """Clean and truncate HTML for LLM processing"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unnecessary elements
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'iframe', 'noscript']):
            tag.decompose()
        
        # Get clean HTML text
        clean_html = str(soup)
        
        # Truncate if too long
        if len(clean_html) > settings.MAX_HTML_LENGTH:
            clean_html = clean_html[:settings.MAX_HTML_LENGTH]
            logger.info(f"HTML truncated to {settings.MAX_HTML_LENGTH} characters")
        
        return clean_html
    
    def _build_extraction_prompt(self, html: str, platform: str, max_reviews: int) -> str:
        """Build prompt for Claude to extract review data"""
        return f"""Extract product review data from this {platform} e-commerce page HTML.

Return ONLY a JSON object with this exact structure (no markdown, no explanation):

{{
  "metadata": {{
    "product_name": "string",
    "platform": "{platform}",
    "total_ratings": number or null,
    "average_rating": number or null,
    "rating_distribution": {{
      "5_star": number,
      "4_star": number,
      "3_star": number,
      "2_star": number,
      "1_star": number
    }} or null
  }},
  "reviews": [
    {{
      "review_id": "string",
      "reviewer_name": "string or null",
      "rating": number (1-5),
      "title": "string or null",
      "text": "string",
      "date": "string or null",
      "verified_purchase": boolean,
      "helpful_count": number
    }}
  ]
}}

Extract up to {max_reviews} reviews. Focus on getting:
- Product name (required)
- Average rating if shown
- Individual reviews with ratings and text (required)
- Any verification badges (verified purchase, etc.)
- Reviewer names if available
- Review dates if available
- Helpful votes if shown

If you cannot find certain fields, use null or 0 as appropriate.

HTML:
{html}"""
    
    async def _call_claude_api(self, prompt: str) -> str:
        """Call Claude API to extract data"""
        async with httpx.AsyncClient(timeout=settings.CLAUDE_TIMEOUT) as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": settings.ANTHROPIC_API_KEY,
                    "anthropic-version": settings.CLAUDE_API_VERSION,
                    "content-type": "application/json"
                },
                json={
                    "model": settings.CLAUDE_MODEL,
                    "max_tokens": settings.CLAUDE_MAX_TOKENS,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"Claude API failed: {response.status_code} - {response.text}")
            
            result = response.json()
            content = result["content"][0]["text"]
            
            logger.info("Successfully extracted data via Claude API")
            return content
    
    def _parse_llm_response(self, content: str) -> Dict[str, Any]:
        """Parse and validate LLM response"""
        try:
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            # Parse JSON
            data = json.loads(content)
            
            # Validate and convert to proper models
            metadata = ProductMetadata(**data["metadata"])
            reviews = [Review(**r) for r in data["reviews"]]
            
            logger.info(f"Parsed {len(reviews)} reviews from LLM response")
            
            return {
                "metadata": metadata,
                "reviews": reviews
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM: {str(e)}")
            logger.error(f"Content: {content[:500]}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="LLM returned invalid JSON"
            )
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to parse LLM response: {str(e)}"
            )