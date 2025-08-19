"""
Configuration settings for Snyk API & Web integration.
"""
import os
from typing import Optional
from dotenv import load_dotenv
import getpass

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Snyk API & Web."""
    
    # API Configuration
    API_BASE_URL = os.getenv("SNYK_API_BASE_URL", "https://api.probely.com")
    API_TOKEN = os.getenv("SNYK_API_TOKEN")
    
    # API Endpoints based on Snyk API & Web documentation
    # https://developers.probely.com/api/reference
    USER_ROLES_BULK_UPDATE_ENDPOINT = "/user-roles/bulk/update/"
    
    # Account endpoints (from Account section)
    ACCOUNT_INFO_ENDPOINT = "/account/"
    ORGANIZATIONS_ENDPOINT = "/orgs/"
    
    # User Roles endpoints (from API Users section)
    # https://developers.probely.com/api/reference/api-user-roles-list
    USER_ROLES_LIST_ENDPOINTS = [
        "/api-user-roles/",
        "/v1/api-user-roles/",
        "/api/v1/api-user-roles/"
    ]
    
    
    # Roles & Permissions endpoints (from Roles & Permissions section)
    ROLES_LIST_ENDPOINTS = [
        "/roles/",
        "/v1/roles/",
        "/api/v1/roles/",
        "/roles-permissions/",
        "/permissions/"
    ]
    
    # Request Configuration
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.API_TOKEN:
            raise ValueError("SNYK_API_TOKEN environment variable is required")
        return True
    
    @classmethod
    def prompt_for_api_token(cls) -> str:
        """Prompt user for API token interactively."""
        token = getpass.getpass("Enter your Snyk API token: ")
        if not token:
            raise ValueError("API token is required")
        cls.API_TOKEN = token
        return token
    
    @classmethod
    def get_headers(cls) -> dict:
        """Get headers for API requests."""
        return {
            "Authorization": f"JWT {cls.API_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
