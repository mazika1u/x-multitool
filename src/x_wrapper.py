import requests
import json
import os
import time
import re
import random
from typing import Dict, List, Optional
from datetime import datetime
from .utils.logger import setup_logger
from .utils.config_manager import ConfigManager

class XWrapper:
    def __init__(self, config_path: str = "config.json"):
        self.logger = setup_logger(__name__)
        self.config_manager = ConfigManager(config_path)
        self.settings = self.config_manager.load_settings()
        
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        }
        
        self.guest_token = None
        self.auth_tokens = {}
        self.csrf_tokens = {}
        
        self.get_guest_token()
    
    def get_guest_token(self):
        try:
            response = self.session.post(
                self.settings['api_endpoints']['guest_token'],
                headers=self.headers
            )
            if response.status_code == 200:
                self.guest_token = response.json()['guest_token']
                self.headers['X-Guest-Token'] = self.guest_token
                self.logger.info("Guest token acquired")
            else:
                self.logger.error(f"Guest token failed: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Guest token error: {e}")
    
    def get_csrf_token(self):
        try:
            response = self.session.get('https://twitter.com/', headers={
                'User-Agent': self.headers['User-Agent']
            })
            match = re.search(r'ct0=([a-f0-9]+)', response.text)
            if match:
                token = match.group(1)
                self.headers['x-csrf-token'] = token
                return token
        except Exception as e:
            self.logger.error(f"CSRF token error: {e}")
        return None
    
    def login(self, username: str, password: str, account_name: str) -> bool:
        try:
            self.get_csrf_token()
            
            flow_headers = self.headers.copy()
            flow_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            # Start login flow
            flow_data = {
                'flow_name': 'login',
                'input_flow_data': json.dumps({
                    'flow_context': {
                        'debug_overrides': {},
                        'start_location': {'location': 'unknown'}
                    },
                    'requested_variant': json.dumps({
                        'type': 'LOGIN_INLINE',
                        'signup_render_trigger': 'impression'
                    })
                })
            }
            
            response = self.session.post(
                self.settings['api_endpoints']['login_flow'],
                headers=flow_headers,
                data=flow_data
            )
            
            if response.status_code != 200:
                self.logger.error(f"Login flow start failed: {response.status_code}")
                return False
                
            flow_data = response.json()
            flow_token = flow_data['flow_token']
            
            # Submit username
            task_data = {
                'flow_token': flow_token,
                'subtask_inputs': [{
                    'subtask_id': 'LoginEnterUserIdentifier',
                    'enter_text': {'text': username, 'link': 'next_link'}
                }]
            }
            
            response = self.session.post(
                self.settings['api_endpoints']['login_flow'],
                headers=flow_headers,
                json=task_data
            )
            
            if response.status_code != 200:
                self.logger.error(f"Username submission failed: {response.status_code}")
                return False
                
            flow_data = response.json()
            flow_token = flow_data['flow_token']
            
            # Submit password
            task_data = {
                'flow_token': flow_token,
                'subtask_inputs': [{
                    'subtask_id': 'LoginEnterPassword',
                    'enter_password': {'password': password, 'link': 'next_link'}
                }]
            }
            
            response = self.session.post(
                self.settings['api_endpoints']['login_flow'],
                headers=flow_headers,
                json=task_data
            )
            
            if response.status_code == 200:
                auth_token = response.cookies.get('auth_token')
                if auth_token:
                    self.auth_tokens[account_name] = auth_token
                    self.csrf_tokens[account_name] = self.headers.get('x-csrf-token', '')
                    
                    # Save to config
                    accounts_data = self.config_manager.load_accounts()
                    if 'accounts' not in accounts_data:
                        accounts_data['accounts'] = {}
                    
                    accounts_data['accounts'][account_name] = {
                        'username': username,
                        'auth_token': auth_token,
                        'csrf_token': self.csrf_tokens[account_name],
                        'last_login': datetime.now().isoformat()
                    }
                    self.config_manager.save_accounts(accounts_data)
                    
                    self.logger.info(f"Login successful: {account_name}")
                    return True
            
            self.logger.error(f"Login failed for {account_name}")
            return False
            
        except Exception as e:
            self.logger.error(f"Login error for {account_name}: {e}")
            return False
    
    def load_saved_account(self, account_name: str) -> bool:
        accounts_data = self.config_manager.load_accounts()
        if account_name in accounts_data.get('accounts', {}):
            account_data = accounts_data['accounts'][account_name]
            self.auth_tokens[account_name] = account_data['auth_token']
            self.csrf_tokens[account_name] = account_data['csrf_token']
            self.logger.info(f"Account loaded: {account_name}")
            return True
        return False
    
    def post_tweet(self, content: str, account_name: str) -> Dict:
        if account_name not in self.auth_tokens:
            raise Exception(f"Account not logged in: {account_name}")
        
        tweet_headers = self.headers.copy()
        tweet_headers['x-csrf-token'] = self.csrf_tokens[account_name]
        tweet_headers['Cookie'] = f'auth_token={self.auth_tokens[account_name]}; ct0={self.csrf_tokens[account_name]}'
        
        tweet_data = {
            'variables': {
                'tweet_text': content,
                'dark_request': False,
                'media': {'media_entities': [], 'possibly_sensitive': False},
                'semantic_annotation_ids': []
            },
            'features': {
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            },
            'queryId': 'SoVnbfCycZ7fERGCwpZkYA'
        }
        
        response = self.session.post(
            self.settings['api_endpoints']['tweet'],
            headers=tweet_headers,
            json=tweet_data
        )
        
        if response.status_code == 200:
            self.logger.info(f"Tweet posted: {account_name}")
            return response.json()
        else:
            self.logger.error(f"Tweet failed: {response.status_code} - {response.text}")
            raise Exception(f"Tweet failed: {response.status_code}")
    
    def post_from_file(self, file_path: str, account_name: str) -> Dict:
        from .utils.file_handler import FileHandler
        file_handler = FileHandler()
        content = file_handler.read_file(file_path)
        if content:
            return self.post_tweet(content, account_name)
        else:
            raise Exception(f"Could not read file: {file_path}")
    
    def reply_to_tweet(self, tweet_id: str, content: str, account_name: str) -> Dict:
        if account_name not in self.auth_tokens:
            raise Exception(f"Account not logged in: {account_name}")
        
        tweet_headers = self.headers.copy()
        tweet_headers['x-csrf-token'] = self.csrf_tokens[account_name]
        tweet_headers['Cookie'] = f'auth_token={self.auth_tokens[account_name]}; ct0={self.csrf_tokens[account_name]}'
        
        reply_data = {
            'variables': {
                'tweet_text': content,
                'reply': {'in_reply_to_tweet_id': tweet_id, 'exclude_reply_user_ids': []},
                'dark_request': False,
                'media': {'media_entities': [], 'possibly_sensitive': False},
                'semantic_annotation_ids': []
            },
            'features': {
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            },
            'queryId': 'SoVnbfCycZ7fERGCwpZkYA'
        }
        
        response = self.session.post(
            self.settings['api_endpoints']['tweet'],
            headers=tweet_headers,
            json=reply_data
        )
        
        if response.status_code == 200:
            self.logger.info(f"Reply posted: {account_name} to {tweet_id}")
            return response.json()
        else:
            self.logger.error(f"Reply failed: {response.status_code}")
            raise Exception(f"Reply failed: {response.status_code}")
