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

# worker that continuously pulls URLs from the queue
async def worker(agent: CrawlAgent, queue: asyncio.Queue):
    while True:
        url = await queue.get()
        try:
            await agent.crawl(url, queue)  # max chaos: await crawl directly
        except Exception as e:
            print(f"[!] Worker error: {e}")
        finally:
            queue.task_done()

async def main():
    crawled = load_crawled()
    print(f"[i] Loaded {len(crawled)} previously crawled URLs.")

    queue = asyncio.Queue()
    for u in seed:
        if u not in crawled:
            await queue.put(u)

    async with aiohttp.ClientSession() as session:
        agent = CrawlAgent(session, crawled_set=crawled)

        # spawn one worker per seed for max chaos speed
        workers = [asyncio.create_task(worker(agent, queue)) for _ in range(len(seed))]

        try:
            await queue.join()  # run until queue is empty
        except KeyboardInterrupt:
            print("\n[i] CTRL+C detected! Shutting down...")
        finally:
            for w in workers:
                w.cancel()
            save_crawled(agent.crawled)
            print(f"[✅] Saved {len(agent.crawled)} URLs.")

if __name__ == "__main__":
    GUSBanner()
    asyncio.run(main())
