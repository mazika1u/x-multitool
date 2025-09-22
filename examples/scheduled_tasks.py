#!/usr/bin/env python3
"""
Scheduled tasks example
"""

import schedule
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.multi_account_manager import MultiAccountManager

def scheduled_post():
    manager = MultiAccountManager()
    manager.login_all()
    manager.bulk_post("data/tweets/daily/morning.txt")

def scheduled_replies():
    manager = MultiAccountManager()
    manager.login_all()
    
    # Reply to new mentions or targets
    manager.bulk_reply("TARGET_TWEET_ID", "data/replies/generic/thank_you.txt")

# Schedule tasks
schedule.every().day.at("09:00").do(scheduled_post)
schedule.every().day.at("14:00").do(scheduled_post)
schedule.every(30).minutes.do(scheduled_replies)

if __name__ == "__main__":
    print("Scheduler started...")
    while True:
        schedule.run_pending()
        time.sleep(60)
