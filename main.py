# main.py
import aiohttp
import asyncio
import json
import os
from agents import CrawlAgent
from seeds import seed
from banner import GUSBanner

DATA_FILE = "crawled.json"

# load already crawled URLs
def load_crawled():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return set(json.load(f))
    return set()

# save crawled URLs
def save_crawled(crawled):
    with open(DATA_FILE, "w") as f:
        json.dump(list(crawled), f, indent=2)

async def main():
    crawled = load_crawled()
    print(f"[i] Loaded {len(crawled)} previously crawled URLs.")

    async with aiohttp.ClientSession() as session:
        agent = CrawlAgent(session, crawled_set=crawled)

        # only crawl seeds that aren't already crawled
        tasks = [agent.crawl(url) for url in seed if url not in crawled]
        results = await asyncio.gather(*tasks)

        # combine all discovered links
        all_discovered = set()
        for link_set in results:
            all_discovered.update(link_set)

        # add seeds + discovered links to crawled set
        agent.crawled.update(all_discovered)

        # save everything to JSON
        save_crawled(agent.crawled)

        print(f"[✅] Total URLs saved (including discovered links): {len(agent.crawled)}")
        print(f"[i] Total new links discovered from seeds: {len(all_discovered)}")

if __name__ == "__main__":
    GUSBanner()
    asyncio.run(main())
