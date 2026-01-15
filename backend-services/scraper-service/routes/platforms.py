"""
Platform information routes
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/supported-platforms")
async def get_supported_platforms():
    """List all supported platforms and scraping methods"""
    return {
        "manual_scraping": [
            {
                "name": "Amazon India",
                "code": "amazon",
                "method": "manual",
                "speed": "fast (2-3 sec)",
                "cost": "free",
                "reliability": "high",
                "example_url": "https://www.amazon.in/dp/B08XYZ123"
            },
            {
                "name": "Flipkart",
                "code": "flipkart",
                "method": "manual",
                "speed": "fast (2-3 sec)",
                "cost": "free",
                "reliability": "high",
                "example_url": "https://www.flipkart.com/product/p/itmXYZ123"
            }
        ],
        "llm_scraping": [
            {
                "name": "Universal (Any E-commerce Site)",
                "method": "llm",
                "provider": "OpenAI ChatGPT",
                "model": "gpt-4o",
                "speed": "moderate (5-10 sec)",
                "cost": "ScrapingBee free tier: 1,000 requests/month + OpenAI API costs",
                "reliability": "excellent",
                "supported_platforms": [
                    "Myntra",
                    "Ajio",
                    "Snapdeal",
                    "Meesho",
                    "Nykaa",
                    "Any other e-commerce site"
                ],
                "requirements": [
                    "SCRAPINGBEE_API_KEY",
                    "OPENAI_API_KEY"
                ]
            }
        ],
        "notes": [
            "For Amazon/Flipkart, manual scraping is used by default (faster, free)",
            "Use force_llm=true in request to test LLM scraping on Amazon/Flipkart",
            "LLM scraping uses OpenAI's ChatGPT (gpt-4o model)",
            "LLM scraping works with any e-commerce site, even unknown ones",
            "Set USE_MOCK_SCRAPER=true for testing without external requests"
        ]
    }