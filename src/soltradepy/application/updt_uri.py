# La entidad coin_info se ha actualizado para incluir los campos uri_size y uri_json. Haz un request a metadata_uri, la cual te devolvera un json. uri_size es el tamaño en bytes de ese json, y uri_json es el json en string.
import asyncio
import json
import logging

import httpx
from sqlmodel import text

from soltradepy.infrastructure.database import get_session
from soltradepy.services.pumpfun.pumpfun_service import PumpfunService

logger = logging.getLogger(__name__)


async def fetch_and_update_metadata(session, service):
    """
    Fetch metadata JSON from each token's metadata_uri,
    calculate its size, and update the database.
    """
    query = "SELECT metadata_uri, mint FROM coin_info WHERE uri_json IS NULL"
    # query = "SELECT metadata_uri, mint FROM coin_info WHERE uri_size = 0 AND metadata_uri LIKE '%ipfs%'  LIMIT 20;"
    metadata_uris = session.execute(text(query)).mappings().all()

    if not metadata_uris:
        logger.info("No tokens found with missing uri_json.")
        return

    proxy = "4.149.153.123:3128"
    proxy = httpx.Proxy(f"http://{proxy}")

    async with httpx.AsyncClient(
        timeout=10.0,
        follow_redirects=True,
    ) as client:
        for row in metadata_uris:
            metadata_uri = row["metadata_uri"]
            mint = row["mint"]
            logger.info(f"Processing mint: {mint} | URI: {metadata_uri}")

            uri_json_str = ""
            uri_size = -1

            try:
                response = await client.get(metadata_uri)
                logger.info(f"Successfully fetched metadata URI: {response}")
                response.raise_for_status()
                uri_json = response.json()
                uri_size = len(uri_json)
                uri_json_str = json.dumps(uri_json, separators=(",", ":"))
                logger.info(f"Fetched metadata for {mint}: {uri_size} size")
            except Exception as e:
                logger.error(f"Error fetching metadata URI {metadata_uri}: {e}")

            await service.sync_uri_data(
                {
                    "uri_size": uri_size,
                    "uri_json": uri_json_str,
                    "mint": mint,
                }
            )


async def main():
    with get_session() as session:
        service = PumpfunService(session=session)
        await fetch_and_update_metadata(session, service)


def cli():
    asyncio.run(main())


if __name__ == "__main__":
    cli()
