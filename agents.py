# agents.py
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio
import random

# random user-agents for stealth
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:91.0) Gecko/20100101 Firefox/91.0",
]

class CrawlAgent:
    def __init__(self, session, base_domain=None, crawled_set=None):
        """
        session: aiohttp session
        base_domain: optional domain restriction
        crawled_set: shared set of already crawled URLs
        """
        self.session = session
        self.base_domain = base_domain
        self.crawled = crawled_set if crawled_set else set()

    async def fetch(self, url, retries=3):
        for attempt in range(retries):
            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                async with self.session.get(url, timeout=10, headers=headers) as r:
                    if r.status == 200 and "text/html" in r.headers.get("Content-Type", ""):
                        return await r.text()
            except Exception as e:
                await asyncio.sleep(0.5 * (attempt + 1))
        print(f"[x] Failed after retries: {url}")
        return None

    def extract_links(self, soup, base_url):
        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            if parsed.scheme not in ("http", "https"):
                continue
            if self.base_domain and self.base_domain not in parsed.netloc:
                continue
            if full_url in self.crawled:
                continue
            links.add(full_url)
        return links

    async def crawl(self, url, queue: asyncio.Queue):
        if url in self.crawled:
            return

        html = await self.fetch(url)
        if not html:
            return

        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "No title"
        print(f"[+] Crawled: {url} → {title}")

        # mark as crawled
        self.crawled.add(url)

        # extract links and add them to queue for recursion
        new_links = self.extract_links(soup, url)
        for link in new_links:
            await queue.put(link)
