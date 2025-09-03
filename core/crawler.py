from bs4 import BeautifulSoup
from core.tor_manager import get_session

def crawl_recursive(url, depth=1, visited=None):
    if visited is None:
        visited = set()

    if depth == 0 or url in visited:
        return []

    visited.add(url)
    session = get_session()
    all_links = []

    try:
        response = session.get(url, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            all_links.extend(links)

            for link in links:
                if link.startswith("http"):
                    all_links.extend(crawl_recursive(link, depth - 1, visited))
    except Exception as e:
        print(f"[!] Error crawling {url}: {e}")

    return all_links
