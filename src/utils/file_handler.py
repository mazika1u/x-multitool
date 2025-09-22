import os
import glob
from typing import List, Optional
from .logger import setup_logger

class FileHandler:
    def __init__(self):
        self.logger = setup_logger(__name__)
        
    def read_file(self, file_path: str) -> Optional[str]:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                self.logger.warning(f"File not found: {file_path}")
                return None
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def write_file(self, file_path: str, content: str):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.logger.info(f"File written: {file_path}")
        except Exception as e:
            self.logger.error(f"Error writing file {file_path}: {e}")
    
    def list_files(self, directory: str, pattern: str = "*.txt") -> List[str]:
        try:
            search_pattern = os.path.join(directory, pattern)
            return glob.glob(search_pattern)
        except Exception as e:
            self.logger.error(f"Error listing files in {directory}: {e}")
            return []
    
    def ensure_data_directories(self):
        directories = [
            'data/tweets/daily',
            'data/tweets/weekly',
            'data/tweets/promotional',
            'data/replies/generic',
            'data/replies/specific',
            'data/targets'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        # Create sample files if they don't exist
        sample_files = {
            'data/tweets/daily/morning.txt': 'Good morning! 🌞\nHave a great day!',
            'data/tweets/daily/afternoon.txt': 'Good afternoon! ☀️\nHow is your day going?',
            'data/replies/generic/thank_you.txt': 'Thank you for your message! 🙏',
            'data/targets/tweet_ids.txt': '# Add tweet IDs here, one per line\n# Example: 1791202943823441920'
        }
        
        for file_path, content in sample_files.items():
            if not os.path.exists(file_path):
                self.write_file(file_path, content)
