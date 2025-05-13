import json
import aiohttp
import asyncio
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
async def fetch_version_manifest(session):
    url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    try:
        async with session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching version manifest: {e}")
        return None

async def fetch_version_details(session, version_url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(version_url, timeout=10) as response:
                response.raise_for_status()
                return await response.json()
            break
        except aiohttp.ClientError as e:
            logger.warning(f"Attempt {attempt + 1} failed for {version_url}: {e}")
            if attempt == retries - 1:
                logger.error(f"Failed to fetch version details for {version_url} after {retries} attempts")
                return None
            await asyncio.sleep(1)

def get_jar_urls(version_data):
    server_url = "Not found"
    client_url = "Not found"
    
    if version_data and "downloads" in version_data:
        downloads = version_data["downloads"]
        server_url = downloads.get("server", {}).get("url", "Not found")
        client_url = downloads.get("client", {}).get("url", "Not found")
    
    return server_url, client_url

async def write_versions(versions):
    header = "# Minecraft Version Download Links\n\n"
    table_header = "| Minecraft Version | Server Jar Download URL | Client Jar Download URL |\n"
    table_separator = "|-------------------|-------------------------|-------------------------|\n"
    
    table_rows = "".join(f"| {v['id']} | {v['server_url']} | {v['client_url']} |\n" for v in versions)
    content = header + table_header + table_separator + table_rows
    
    os.makedirs("temp", exist_ok=True)
    versions_path = os.path.join("temp", "versions.md")

    with ThreadPoolExecutor() as pool:
        await asyncio.get_event_loop().run_in_executor(pool, lambda: open(versions_path, "w", encoding="utf-8").write(content))
    
    logger.info(f"versions.md generated at {versions_path}")

async def process_version(session, version, semaphore):
    async with semaphore:
        version_id = version["id"]
        version_url = version["url"]
        logger.info(f"Fetching details for version {version_id}")
        version_data = await fetch_version_details(session, version_url)
        
        if version_data:
            server_url, client_url = get_jar_urls(version_data)
            return {
                "id": version_id,
                "releaseTime": version.get("releaseTime", ""),
                "server_url": server_url,
                "client_url": client_url
            }
        return None

async def main():
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        manifest = await fetch_version_manifest(session)
        if not manifest:
            return

        tasks = [process_version(session, version, semaphore) for version in manifest["versions"]]
        versions = [v for v in await asyncio.gather(*tasks, return_exceptions=True) if v and not isinstance(v, Exception)]

        versions.sort(key=lambda x: x["releaseTime"], reverse=True)
        
        await write_versions(versions)

if __name__ == "__main__":
    asyncio.run(main())
