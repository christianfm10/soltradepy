import logging
from pathlib import Path

import nodriver as uc
from nodriver.cdp.network import Cookie

logger = logging.getLogger(__name__)


class CloudflareBypass:
    """
    Manages browser automation for bypassing Cloudflare protection
    and obtaining cf_clearance cookies.
    """

    def __init__(
        self,
        target_url: str,
        proxy: str | None = None,
        headless: bool = False,
        session_dir: str = "sessions",
        timeout: int = 100,
    ):
        self.target_url = target_url
        self.proxy = proxy
        self.headless = headless
        self.timeout = timeout

        # Initialize session path
        session_id = proxy.replace(":", "_").replace("/", "_") if proxy else "default"
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(exist_ok=True)
        self.session_file = self.session_dir / f"session_{session_id}.dat"

        # Browser state
        self.browser: uc.Browser | None = None
        self.tab: uc.Tab | None = None
        self.user_agent: str | None = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "Chrome/137.0.0.0 Safari/537.36"
        )
        self.cf_clearance: Cookie | None = None

    async def initialize_browser(self):
        """Initialize browser with custom configuration"""
        browser_args = [
            "--disable-popup-blocking",
            "--ignore-ssl-errors",
            "--ignore-certificate-errors",
        ]

        if self.proxy:
            browser_args.append(f"--proxy-server={self.proxy}")

        self.browser = await uc.start(browser_args=browser_args, headless=self.headless)
        self.user_agent = self.browser.info.get("User-Agent", "")
        logger.debug(f"Browser initialized with UA: {self.user_agent}")

    async def load_session(self):
        """Load previous session if exists"""
        if self.session_file.exists():
            await self.browser.cookies.load(str(self.session_file), pattern="cf")
            logger.debug(f"Loaded session from {self.session_file}")

    async def save_session(self):
        """Save current session for future use"""
        await self.browser.cookies.save(str(self.session_file), pattern="cf")
        logger.debug(f"Saved session to {self.session_file}")

    async def get_cf_clearance(self) -> bool:
        """Get cf_clearance cookie"""
        cookies = await self.browser.cookies.get_all(requests_cookie_format=True)
        for cookie in cookies:
            if cookie.name == "cf_clearance":
                self.cf_clearance = cookie
                logger.info("Successfully obtained cf_clearance cookie")
                return True
        logger.warning("No cf_clearance cookie found")
        return False

    async def navigate_to_target(self) -> bool:
        """Navigate to target URL and handle Cloudflare"""
        try:
            # Verify proxy is working
            self.tab_ip = await self.browser.get("https://httpbin.org/ip")

            # Navigate to target
            self.tab = await self.browser.get(self.target_url, new_tab=True)

            # Wait for page load or error
            await self.tab.wait_for(
                text="The page could not be found", timeout=self.timeout
            )
            return True

        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return False

    async def close(self):
        """Clean up browser resources"""
        if self.tab:
            await self.tab.close()
        if self.browser:
            self.browser.stop()

    async def run(self, update_cf: bool = True) -> bool:
        """Main execution flow"""
        try:
            await self.initialize_browser()
            await self.load_session()

            if update_cf and not await self.navigate_to_target():
                return False

            if not await self.get_cf_clearance():
                logger.error("Failed to obtain cf_clearance cookie")
                return False

            await self.save_session()
            return True

        except Exception as e:
            logger.exception(f"Error during execution: {e}")
            return False

        finally:
            await self.close()
