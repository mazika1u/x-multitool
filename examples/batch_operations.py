#!/usr/bin/env python3
"""
Batch operations example
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.multi_account_manager import MultiAccountManager

def batch_operations():
    manager = MultiAccountManager()
    
    # Add accounts
    manager.add_account("account1", "user1", "pass1")
    manager.add_account("account2", "user2", "pass2")
    
    # Login
    manager.login_all()
    
    # Batch post from directory
    manager.batch_post_from_directory("data/tweets/daily")
    
    # Reply to multiple tweets
    with open("data/targets/tweet_ids.txt", "r") as f:
        tweet_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    for tweet_id in tweet_ids:
        manager.bulk_reply(tweet_id, "data/replies/generic/thank_you.txt")

if __name__ == "__main__":
    batch_operations()
