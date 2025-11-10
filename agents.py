# agents.py
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio

class CrawlAgent:
    def __init__(self, session, base_domain=None, crawled_set=None):
        """
        session: aiohttp session
        base_domain: optional, only follow links within this domain
        crawled_set: a set of URLs already crawled (to skip duplicates)
        """
        self.session = session
        self.base_domain = base_domain
        self.crawled = crawled_set if crawled_set is not None else set()

    async def fetch(self, url):
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status == 200 and "text/html" in response.headers.get("Content-Type", ""):
                    return await response.text()
        except Exception as e:
            print(f"[x] Error fetching {url}: {e}")
        return None

    def extract_links(self, soup, base_url):
        links = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            parsed = urlparse(full_url)
            if parsed.scheme in ("http", "https"):
                # skip already crawled
                if full_url in self.crawled:
                    continue
                # optional domain filter
                if self.base_domain and self.base_domain not in parsed.netloc:
                    continue
                links.add(full_url)
        return links

    async def crawl(self, url):
        if url in self.crawled:
            print(f"[↩] Skipping {url} (already crawled)")
            return set()

        html = await self.fetch(url)
        if not html:
            return set()

        soup = BeautifulSoup(html, "html.parser")

        # fully safe title extraction
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        else:
            title = "No title"

        print(f"[+] Crawled: {url} → {title}")

        # mark as crawled
        self.crawled.add(url)

        # extract links
        new_links = self.extract_links(soup, url)
        return new_links
