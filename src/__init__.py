"""
X Account Manager - Multi-account management tool for X (Twitter)
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .x_wrapper import XWrapper
from .multi_account_manager import MultiAccountManager

__all__ = ["XWrapper", "MultiAccountManager"]
