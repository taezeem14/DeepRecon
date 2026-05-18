"""AI Analysis core utilizing LLMs to synthesize OSINT data."""

from __future__ import annotations
import os
import requests

from config import (
    USER_AGENT, 
    AI_PROVIDER, 
    AI_MODEL, 
    OPENAI_API_KEY, 
    ANTHROPIC_API_KEY, 
    OPENROUTER_API_KEY, 
    OLLAMA_URL
)
from utils.logger import logger

class AIAnalyzer:
    """Class exposing basic LLM summarization patterns."""
    
    def __init__(self):
        self.provider = AI_PROVIDER.lower()
        self.ollama_url = OLLAMA_URL
        
    def generate_investigation_summary(self, target_url: str, text_content: str, metadata: dict) -> str:
        """Query LLM to generate an automated OSINT summary from scraped data."""
        if not text_content:
            return "No text available for AI analysis."
            
        system_prompt = "You are a cybersecurity expert analyzing Dark Web content."
        user_prompt = (
            f"Target URL: {target_url}\n"
            f"Extracted Metadata (Crypto/Emails/PGP): {metadata}\n\n"
            f"Page Content Snippet:\n{text_content[:3000]}\n\n"
            f"Provide a short, analytical summary of the threat landscape surrounding this node."
        )
        
        try:
            if self.provider == "openai":
                return self._query_openai(system_prompt, user_prompt)
            elif self.provider == "anthropic":
                return self._query_anthropic(system_prompt, user_prompt)
            elif self.provider == "openrouter":
                return self._query_openrouter(system_prompt, user_prompt)
            else:
                return self._query_ollama(system_prompt, user_prompt)
        except Exception as e:
            logger.error(f"AI Analyzer error: {e}")
            return f"AI Analysis unavailable using provider '{self.provider}'."

    def _query_ollama(self, system: str, user: str) -> str:
        model = AI_MODEL or "llama3"
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={"model": model, "prompt": f"{system}\n\n{user}", "stream": False},
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get("response", "AI response empty.")
        return "Failed to query Ollama (ensure it is running and model exists)."

    def _query_openai(self, system: str, user: str) -> str:
        if not OPENAI_API_KEY:
            return "OpenAI API Key not configured."
        model = AI_MODEL or "gpt-4o"
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"OpenAI API Error: {response.status_code} - {response.text}"

    def _query_anthropic(self, system: str, user: str) -> str:
        if not ANTHROPIC_API_KEY:
            return "Anthropic API Key not configured."
        model = AI_MODEL or "claude-3-haiku-20240307"
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY, 
                "anthropic-version": "2023-06-01", 
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "system": system,
                "messages": [{"role": "user", "content": user}],
                "max_tokens": 1024
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        return f"Anthropic API Error: {response.status_code} - {response.text}"

    def _query_openrouter(self, system: str, user: str) -> str:
        if not OPENROUTER_API_KEY:
            return "OpenRouter API Key not configured."
        model = AI_MODEL or "openai/gpt-4o-mini"
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"OpenRouter API Error: {response.status_code} - {response.text}"