import pytest

from soltradepy.infrastructure.browser.cloudflare_bypass import CloudflareBypass
from soltradepy.infrastructure.config.env import get_settings

settings = get_settings()


# ['41.89.56.116:3128', '211.230.49.122:3128', '176.126.103.194:44214', '95.216.214.204:8888', '186.180.73.50:9090', '178.32.123.218:1080', '41.223.119.156:3128', '205.237.104.203:3128', '185.41.152.110:3128', '60.249.94.59:3128']
async def get_cf_cookie(proxy: str):
    cf_bypass = CloudflareBypass(
        target_url="https://solscan.io/account/", proxy=proxy, headless=True
    )

    success = await cf_bypass.run()
    if success:
        return cf_bypass.cf_clearance
    return None


@pytest.mark.asyncio
@pytest.mark.skip
async def test_cf_bypass():
    proxy = "95.216.214.204:8888"
    cf_bypass = CloudflareBypass(
        target_url="https://solscan.io/account/", proxy=proxy, headless=False
    )

    success = await cf_bypass.run()

    assert success
