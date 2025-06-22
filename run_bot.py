#!/usr/bin/env python3
"""
Standalone script to run the Telegram bot for receiving commands from users.
This script should be run separately from the main Flask application.
"""

import os
import logging
from telegram_bot import run_bot_polling

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    print("Starting Telegram bot...")
    print("Bot will listen for:")
    print("- /start - Subscribe to document notifications")
    print("- /stop - Unsubscribe from notifications") 
    print("- /status - Check subscription status")
    print("\nPress Ctrl+C to stop the bot")
    
    try:
        run_bot_polling()
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Bot error: {e}")