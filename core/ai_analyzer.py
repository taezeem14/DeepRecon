"""AI Analysis core utilizing LLMs to synthesize OSINT data."""

from __future__ import annotations

import os
import requests
from typing import Any

from config import (
    USER_AGENT, 
    AI_PROVIDER, 
    AI_MODEL, 
    OPENAI_API_KEY, 
    ANTHROPIC_API_KEY, 
    OPENROUTER_API_KEY, 
    GEMINI_API_KEY,
    OLLAMA_URL
)
from utils.logger import get_logger

LOGGER = get_logger(__name__)


class AIAnalyzer:
    """Multi-provider LLM analysis engine for Dark Web threat triage."""
    
    def __init__(self, provider: str | None = None, model: str | None = None):
        self.provider = (provider or AI_PROVIDER).lower()
        self.model = model or AI_MODEL
        self.ollama_url = OLLAMA_URL
        
    def generate_investigation_summary(self, target_url: str, text_content: str, metadata: dict[str, Any] | None = None) -> str:
        """Query LLM or fallback heuristics to generate an automated OSINT summary."""
        metadata = metadata or {}
        if not text_content and not metadata:
            return "No content or metadata available for OSINT analysis."
            
        system_prompt = (
            "You are DeepRecon AI, an elite cybersecurity and threat intelligence expert "
            "analyzing Dark Web / Tor network intelligence. Summarize threat indicators, key services, "
            "identified infrastructure, operational security observations, and actionable leads concisely."
        )
        
        user_prompt = (
            f"Target URL: {target_url}\n"
            f"Extracted Metadata (Crypto/Emails/PGP/Tech): {metadata}\n\n"
            f"Page Content Snippet:\n{text_content[:4000]}\n\n"
            f"Provide a structured OSINT threat intelligence assessment covering:\n"
            f"1. Executive Summary & Domain Purpose\n"
            f"2. Threat / Risk Classification (Low / Medium / High / Critical)\n"
            f"3. Identified Artifacts (Crypto Wallets, Emails, Tech Stacks)\n"
            f"4. Key Findings & Recommended Pivot Vectors"
        )
        
        try:
            if self.provider == "openai":
                return self._query_openai(system_prompt, user_prompt)
            elif self.provider == "anthropic":
                return self._query_anthropic(system_prompt, user_prompt)
            elif self.provider == "openrouter":
                return self._query_openrouter(system_prompt, user_prompt)
            elif self.provider == "gemini":
                return self._query_gemini(system_prompt, user_prompt)
            elif self.provider == "ollama":
                return self._query_ollama(system_prompt, user_prompt)
            else:
                return self._generate_heuristic_summary(target_url, text_content, metadata)
        except Exception as e:
            LOGGER.debug(f"AI Analyzer query error: {e}")
            return self._generate_heuristic_summary(target_url, text_content, metadata)

    def _query_ollama(self, system: str, user: str) -> str:
        model = self.model or "llama3"
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={"model": model, "prompt": f"{system}\n\n{user}", "stream": False},
            timeout=30
        )
        if response.status_code == 200:
            res_text = response.json().get("response", "").strip()
            if res_text:
                return res_text
        raise ConnectionError(f"Ollama returned status {response.status_code}")

    def _query_openai(self, system: str, user: str) -> str:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API Key not configured.")
        model = self.model or "gpt-4o"
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "temperature": 0.3
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        raise RuntimeError(f"OpenAI API Error: {response.status_code} - {response.text}")

    def _query_anthropic(self, system: str, user: str) -> str:
        if not ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API Key not configured.")
        model = self.model or "claude-3-haiku-20240307"
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
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["content"][0]["text"]
        raise RuntimeError(f"Anthropic API Error: {response.status_code} - {response.text}")

    def _query_openrouter(self, system: str, user: str) -> str:
        if not OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API Key not configured.")
        model = self.model or "openai/gpt-4o-mini"
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        raise RuntimeError(f"OpenRouter API Error: {response.status_code} - {response.text}")

    def _query_gemini(self, system: str, user: str) -> str:
        api_key = GEMINI_API_KEY or os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise ValueError("Gemini API Key not configured.")
        model = self.model or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": f"{system}\n\n{user}"}]}]
            },
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
        raise RuntimeError(f"Gemini API Error: {response.status_code} - {response.text}")

    def _generate_heuristic_summary(self, target_url: str, text_content: str, metadata: dict[str, Any]) -> str:
        """Deterministic OSINT heuristic triage summary when remote LLM is offline."""
        crypto = metadata.get("crypto", {}) or metadata.get("crypto_addresses", {})
        emails = metadata.get("emails", [])
        pgp = metadata.get("pgp", []) or metadata.get("pgp_blocks", [])
        tech = metadata.get("technologies", []) or metadata.get("detected_technologies", [])
        
        btc_count = len(crypto.get("bitcoin", []))
        eth_count = len(crypto.get("ethereum", []))
        xmr_count = len(crypto.get("monero", []))
        total_crypto = btc_count + eth_count + xmr_count

        risk_level = "LOW"
        if total_crypto > 0 or len(pgp) > 0:
            risk_level = "MEDIUM"
        if (btc_count > 2 or xmr_count > 0) and any(w in text_content.lower() for w in ["market", "escrow", "vendor", "leak", "dump", "carding"]):
            risk_level = "HIGH"

        lines = [
            f"🔍 [b]DeepRecon OSINT Threat Summary (Automated Triage)[/b]",
            f"• Target Node: {target_url}",
            f"• Risk Classification: {risk_level}",
            f"• Crypto Artifacts: {total_crypto} total (BTC: {btc_count}, ETH: {eth_count}, XMR: {xmr_count})",
            f"• Email Addresses: {len(emails)} discovered ({', '.join(emails[:3]) if emails else 'None'})",
            f"• PGP Key Blocks: {'Present (' + str(len(pgp)) + ')' if pgp else 'None'}",
            f"• Fingerprinted Tech: {', '.join(tech) if tech else 'Generic / Hidden'}",
            f"• Payload Size: {len(text_content)} characters analyzed",
        ]
        return "\n".join(lines)