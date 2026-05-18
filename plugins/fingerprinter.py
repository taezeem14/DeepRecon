import re
from typing import Any
from plugins import BasePlugin


class FingerprinterPlugin(BasePlugin):
    """
    Identifies technology stacks (e.g., WordPress, Nginx, PHP, React) from page content,
    headers, and meta tags.
    """

    # Basic signatures mapped to a technology
    SIGNATURES = {
        "WordPress": [r"wp-content", r"wp-includes", r"generator..WordPress"],
        "PHP": [r"\.php", r"PHPSESSID"],
        "Nginx": [r"Server..nginx", r"nginx/1\."],
        "Apache": [r"Server..Apache", r"Apache/2\."],
        "React": [r"data-reactroot", r"react-dom\.production"],
        "Cloudflare": [r"cf-ray", r"cloudflare-nginx"],
        "Joomla": [r"Joomla!", r"joomla\.xml"],
        "Drupal": [r"Drupal\.settings", r"sites/all/modules"],
        "MySQL": [r"SQL syntax.*MySQL", r"Warning.*mysql_"],
    }

    @property
    def name(self) -> str:
        return "fingerprinter"

    @property
    def description(self) -> str:
        return "Identifies technology stack based on signatures in the HTML."

    def extract(self, page) -> dict[str, Any]:
        identified_tech = set()
        
        # Searching through the raw HTML to catch meta tags, script names, etc.
        for tech, patterns in self.SIGNATURES.items():
            for pattern in patterns:
                if re.search(pattern, page.raw_html, re.IGNORECASE):
                    identified_tech.add(tech)
                    break  # Found at least one signature for this tech

        return {"detected_technologies": list(identified_tech)}

PLUGIN_CLASS = FingerprinterPlugin

