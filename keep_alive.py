import asyncio
import aiohttp
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class KeepAlive:
    """Keep the application alive by making periodic requests"""
    
    def __init__(self, url="http://localhost:5000", interval=60):
        self.url = url
        self.interval = interval
        self.running = True
        
    async def ping(self):
        """Send a ping request to keep the service alive"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.url}/api/status", timeout=10) as response:
                    if response.status == 200:
                        logger.info(f"💓 Keep-alive ping successful at {datetime.now()}")
                    else:
                        logger.warning(f"⚠️ Keep-alive ping returned status {response.status}")
        except Exception as e:
            logger.error(f"❌ Keep-alive ping failed: {e}")
    
    async def start(self):
        """Start the keep-alive service"""
        logger.info(f"🔄 Starting keep-alive service (pinging every {self.interval} seconds)")
        
        while self.running:
            await self.ping()
            await asyncio.sleep(self.interval)
    
    def stop(self):
        """Stop the keep-alive service"""
        self.running = False
        logger.info("⏹️ Keep-alive service stopped")

# Global keep-alive instance
keep_alive = KeepAlive()

def start_keep_alive():
    """Start keep-alive in a separate thread"""
    try:
        asyncio.run(keep_alive.start())
    except Exception as e:
        logger.error(f"❌ Keep-alive service crashed: {e}")
        time.sleep(5)
        start_keep_alive()  # Restart on failure