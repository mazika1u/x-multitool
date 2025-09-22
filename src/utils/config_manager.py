import json
import os
from typing import Dict, Any
from .logger import setup_logger

class ConfigManager:
    def __init__(self, config_path: str = "config.json"):
        self.logger = setup_logger(__name__)
        self.config_path = config_path
        self.settings_path = "config/settings.json"
        self.accounts_path = "config/accounts.json"
        self._ensure_directories()
        
    def _ensure_directories(self):
        os.makedirs('config', exist_ok=True)
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data/tweets/daily', exist_ok=True)
        os.makedirs('data/replies/generic', exist_ok=True)
        os.makedirs('data/targets', exist_ok=True)
        
    def load_settings(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.settings_path):
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.logger.warning("Settings file not found, using defaults")
                return self._get_default_settings()
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            return self._get_default_settings()
    
    def load_accounts(self) -> Dict[str, Any]:
        try:
            if os.path.exists(self.accounts_path):
                with open(self.accounts_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Error loading accounts: {e}")
            return {}
    
    def save_accounts(self, accounts_data: Dict[str, Any]):
        try:
            with open(self.accounts_path, 'w', encoding='utf-8') as f:
                json.dump(accounts_data, f, indent=2, ensure_ascii=False)
            self.logger.info("Accounts config saved")
        except Exception as e:
            self.logger.error(f"Error saving accounts: {e}")
    
    def _get_default_settings(self) -> Dict[str, Any]:
        return {
            "api_endpoints": {
                "guest_token": "https://api.twitter.com/1.1/guest/activate.json",
                "login_flow": "https://api.twitter.com/1.1/onboarding/task.json",
                "tweet": "https://twitter.com/i/api/graphql/SoVnbfCycZ7fERGCwpZkYA/CreateTweet",
            },
            "rate_limits": {
                "post_delay_min": 3,
                "post_delay_max": 7,
                "reply_delay_min": 5,
                "reply_delay_max": 10,
            }
        }
