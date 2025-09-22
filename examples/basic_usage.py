#!/usr/bin/env python3
"""
Basic usage example for X Account Manager
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.multi_account_manager import MultiAccountManager

def main():
    # Initialize manager
    manager = MultiAccountManager()
    
    # Add accounts
    manager.add_account("main", "your_username1", "your_password1")
    manager.add_account("backup", "your_username2", "your_password2")
    
    # Login
    print("Logging in...")
    manager.login_all()
    
    # Post from file
    print("Posting...")
    manager.bulk_post("data/tweets/daily/morning.txt")
    
    print("Operation completed!")

if __name__ == "__main__":
    main()
