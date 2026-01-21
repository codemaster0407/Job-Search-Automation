import asyncio
from crawl4ai import *
import Config
from utils.string_parser import extract_https_links
async def main(url, max_depth = 10):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
            max_depth = max_depth
        )
        if Config.LOG  :
            print(result.markdown)
    return str(result.markdown)
def start_async_crawl(url, md = 10):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main(url, max_depth=md))
    links = extract_https_links(result)
    return links    


def start_job_crawl(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main(url, max_depth=0))
    return str(result)
