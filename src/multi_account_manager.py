import time
import random
from typing import List, Dict, Optional
from .x_wrapper import XWrapper
from .utils.logger import setup_logger
from .utils.file_handler import FileHandler

class MultiAccountManager:
    def __init__(self, config_path: str = "config.json"):
        self.logger = setup_logger(__name__)
        self.file_handler = FileHandler()
        self.wrapper = XWrapper(config_path)
        self.accounts = {}
        self.settings = self.wrapper.settings
        
    def add_account(self, name: str, username: str, password: str):
        self.accounts[name] = {'username': username, 'password': password}
        self.logger.info(f"Account added: {name}")
    
    def login_all(self, force_fresh: bool = False):
        for name, creds in self.accounts.items():
            if not force_fresh and self.wrapper.load_saved_account(name):
                continue
                
            success = self.wrapper.login(creds['username'], creds['password'], name)
            if success:
                delay = self.settings['rate_limits']['login_delay']
                time.sleep(delay)
            else:
                self.logger.error(f"Login failed: {name}")
    
    def bulk_post(self, file_path: str, account_names: List[str] = None):
        if account_names is None:
            account_names = list(self.accounts.keys())
        
        for account_name in account_names:
            try:
                result = self.wrapper.post_from_file(file_path, account_name)
                self.logger.info(f"{account_name}: Posted successfully")
                
                delay_min = self.settings['rate_limits']['post_delay_min']
                delay_max = self.settings['rate_limits']['post_delay_max']
                time.sleep(random.uniform(delay_min, delay_max))
                
            except Exception as e:
                self.logger.error(f"{account_name}: Failed - {e}")
    
    def bulk_reply(self, tweet_id: str, file_path: str, account_names: List[str] = None):
        if account_names is None:
            account_names = list(self.accounts.keys())
        
        for account_name in account_names:
            try:
                content = self.file_handler.read_file(file_path)
                if content:
                    result = self.wrapper.reply_to_tweet(tweet_id, content, account_name)
                    self.logger.info(f"{account_name}: Replied successfully")
                    
                    delay_min = self.settings['rate_limits']['reply_delay_min']
                    delay_max = self.settings['rate_limits']['reply_delay_max']
                    time.sleep(random.uniform(delay_min, delay_max))
                else:
                    self.logger.error(f"Could not read reply file: {file_path}")
                    
            except Exception as e:
                self.logger.error(f"{account_name}: Reply failed - {e}")
    
    def batch_post_from_directory(self, directory: str, account_names: List[str] = None):
        files = self.file_handler.list_files(directory)
        for file_path in files:
            self.logger.info(f"Posting from: {file_path}")
            self.bulk_post(file_path, account_names)
            time.sleep(10)
