import asyncio
import threading
import time
import logging
import sys
import signal
from web_server import start_web_server
from keep_alive import start_keep_alive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def start_bot_with_recovery():
    """Start the bot with automatic recovery and restart capabilities."""
    restart_count = 0
    
    while True:  # Infinite restart attempts
        try:
            logger.info(f"🚀 Starting Discord bot (attempt {restart_count + 1})")
            import bot
            
            # Keep the bot running and monitor health
            last_health_check = time.time()
            while True:
                time.sleep(1)
                
                # Health check every 30 seconds
                if time.time() - last_health_check > 30:
                    if hasattr(bot, 'bot') and bot.bot.is_ready():
                        logger.debug("💓 Bot health check passed")
                    else:
                        logger.warning("⚠️ Bot health check failed, triggering restart")
                        raise Exception("Bot health check failed")
                    last_health_check = time.time()
                
        except KeyboardInterrupt:
            logger.info("👋 Shutting down...")
            break
        except Exception as e:
            restart_count += 1
            logger.error(f"❌ Bot crashed: {e}")
            
            # Progressive backoff, but always restart
            wait_time = min(10 + (restart_count * 5), 120)  # Start at 10s, max 2 minutes
            logger.info(f"🔄 Restarting bot in {wait_time} seconds... (attempt {restart_count})")
            time.sleep(wait_time)
            
            # Clean up and reload bot module
            try:
                import sys
                if 'bot' in sys.modules:
                    del sys.modules['bot']
                    logger.info("🧹 Bot module cleaned up")
            except Exception as cleanup_error:
                logger.warning(f"⚠️ Cleanup warning: {cleanup_error}")

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"📢 Received signal {signum}, shutting down gracefully...")
    sys.exit(0)

def main():
    """
    Main entry point that starts all services with maximum reliability.
    """
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("🚀 Starting Marble Burger House Discord Bot with maximum uptime features")
    
    # Start the web server in a separate thread
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    logger.info("🌐 Web server started on http://0.0.0.0:5000")
    
    # Start keep-alive service in a separate thread
    keep_alive_thread = threading.Thread(target=start_keep_alive, daemon=True)
    keep_alive_thread.start()
    logger.info("💓 Keep-alive service started")
    
    # Start bot in a separate thread with recovery
    bot_thread = threading.Thread(target=start_bot_with_recovery, daemon=False)
    bot_thread.start()
    logger.info("🤖 Discord bot started with auto-recovery")
    
    # Main monitoring loop
    last_thread_check = time.time()
    try:
        while True:
            current_time = time.time()
            
            # Check threads every 30 seconds
            if current_time - last_thread_check > 30:
                threads_status = []
                
                if not web_thread.is_alive():
                    logger.error("❌ Web server thread died, restarting...")
                    web_thread = threading.Thread(target=start_web_server, daemon=True)
                    web_thread.start()
                    threads_status.append("Web: RESTARTED")
                else:
                    threads_status.append("Web: OK")
                
                if not keep_alive_thread.is_alive():
                    logger.error("❌ Keep-alive thread died, restarting...")
                    keep_alive_thread = threading.Thread(target=start_keep_alive, daemon=True)
                    keep_alive_thread.start()
                    threads_status.append("KeepAlive: RESTARTED")
                else:
                    threads_status.append("KeepAlive: OK")
                
                if not bot_thread.is_alive():
                    logger.error("❌ Bot thread died, restarting...")
                    bot_thread = threading.Thread(target=start_bot_with_recovery, daemon=False)
                    bot_thread.start()
                    threads_status.append("Bot: RESTARTED")
                else:
                    threads_status.append("Bot: OK")
                
                logger.info(f"🔍 System status: {' | '.join(threads_status)}")
                last_thread_check = current_time
            
            time.sleep(1)  # Check frequently
            
    except KeyboardInterrupt:
        logger.info("👋 Graceful shutdown initiated...")
    except Exception as e:
        logger.error(f"❌ Main loop crashed: {e}, restarting...")
        main()  # Restart the entire application

if __name__ == "__main__":
    main()