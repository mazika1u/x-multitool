#!/usr/bin/env python3
"""
X Account Manager - Main executable
"""

import argparse
import sys
import os
from src.multi_account_manager import MultiAccountManager
from src.utils.file_handler import FileHandler

def main():
    parser = argparse.ArgumentParser(description='X Account Manager')
    parser.add_argument('--config', default='config.json', help='Config file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add account command
    add_parser = subparsers.add_parser('add-account', help='Add new account')
    add_parser.add_argument('--name', required=True, help='Account nickname')
    add_parser.add_argument('--username', required=True, help='X username')
    add_parser.add_argument('--password', required=True, help='X password')
    
    # Post command
    post_parser = subparsers.add_parser('post', help='Post from file')
    post_parser.add_argument('--file', required=True, help='File containing tweet content')
    post_parser.add_argument('--accounts', nargs='+', help='Specific accounts to use')
    
    # Reply command
    reply_parser = subparsers.add_parser('reply', help='Reply to tweet')
    reply_parser.add_argument('--tweet-id', required=True, help='Tweet ID to reply to')
    reply_parser.add_argument('--file', required=True, help='File containing reply content')
    reply_parser.add_argument('--accounts', nargs='+', help='Specific accounts to use')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        file_handler = FileHandler()
        file_handler.ensure_data_directories()
        
        manager = MultiAccountManager(args.config)
        
        if args.command == 'add-account':
            manager.add_account(args.name, args.username, args.password)
            manager.login_all()
            print(f"Account '{args.name}' added and logged in successfully")
            
        elif args.command == 'post':
            manager.login_all()
            manager.bulk_post(args.file, args.accounts)
            print("Posting completed")
            
        elif args.command == 'reply':
            manager.login_all()
            manager.bulk_reply(args.tweet_id, args.file, args.accounts)
            print("Replying completed")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
