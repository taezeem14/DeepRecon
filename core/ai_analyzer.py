"""AI Analysis core utilizing LLMs to synthesize OSINT data."""

from __future__ import annotations
import os
import requests

from config import USER_AGENT
from utils.logger import logger

class AIAnalyzer:
    """Class exposing basic LLM summarization patterns."""
    
    def __init__(self, ollama_url: str = "http://127.0.0.1:11434"):
        self.ollama_url = ollama_url
        self.model = os.getenv("OLLAMA_MODEL", "llama3")
        
    def generate_investigation_summary(self, target_url: str, text_content: str, metadata: dict) -> str:
        """Query LLM to generate an automated OSINT summary from scraped data."""
        if not text_content:
            return "No text available for AI analysis."
            
        prompt = (
            f"You are a cybersecurity expert analyzing Dark Web content.\n"
            f"Target URL: {target_url}\n"
            f"Extracted Metadata (Crypto/Emails/PGP): {metadata}\n\n"
            f"Page Content Snippet:\n{text_content[:3000]}\n\n"
            f"Provide a short, analytical summary of the threat landscape surrounding this node."
        )
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "AI response empty.")
            else:
                return "Failed to query AI module (Ollama not running or model missing)."
        except Exception as e:
            logger.error(f"AI Analyzer error: {e}")
            return "AI Analysis unavailable."