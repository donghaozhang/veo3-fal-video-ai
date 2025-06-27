"""
API Helper Utilities

Common utilities for API interactions and request handling.
"""

import time
import requests
from typing import Dict, Optional, Any
import json


def validate_api_key(api_key: str) -> bool:
    """
    Validate that an API key is properly formatted.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not isinstance(api_key, str):
        return False
    
    # Basic validation - ElevenLabs API keys are typically 32+ characters
    if len(api_key) < 20:
        return False
    
    return True


def make_request_with_retry(
    url: str,
    headers: Dict[str, str],
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    method: str = "POST",
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> Optional[requests.Response]:
    """
    Make an HTTP request with retry logic.
    
    Args:
        url: Request URL
        headers: Request headers
        data: Request data (for JSON requests)
        files: Request files (for multipart requests)
        method: HTTP method
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        Response object if successful, None otherwise
    """
    for attempt in range(max_retries + 1):
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                if files:
                    # Remove Content-Type for multipart requests
                    headers_copy = headers.copy()
                    headers_copy.pop("Content-Type", None)
                    response = requests.post(url, headers=headers_copy, data=data, files=files, timeout=60)
                elif data:
                    response = requests.post(url, headers=headers, json=data, timeout=60)
                else:
                    response = requests.post(url, headers=headers, timeout=60)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check if request was successful
            if response.status_code in [200, 201]:
                return response
            elif response.status_code == 429:  # Rate limit
                if attempt < max_retries:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limited. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    continue
            else:
                print(f"HTTP {response.status_code}: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                print(f"Request failed (attempt {attempt + 1}): {e}")
                time.sleep(retry_delay)
                continue
            else:
                print(f"Request failed after {max_retries + 1} attempts: {e}")
                return None
    
    return None


def parse_api_error(response: requests.Response) -> str:
    """
    Parse API error response and return user-friendly message.
    
    Args:
        response: Failed response object
        
    Returns:
        Error message string
    """
    try:
        error_data = response.json()
        if isinstance(error_data, dict):
            # Try common error message fields
            error_msg = error_data.get('detail') or error_data.get('message') or error_data.get('error')
            if error_msg:
                return str(error_msg)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # Fallback to HTTP status and raw text
    return f"HTTP {response.status_code}: {response.text[:200]}"


def build_headers(api_key: str, content_type: str = "application/json") -> Dict[str, str]:
    """
    Build standard headers for ElevenLabs API requests.
    
    Args:
        api_key: ElevenLabs API key
        content_type: Content type for the request
        
    Returns:
        Headers dictionary
    """
    return {
        "Accept": "audio/mpeg",
        "Content-Type": content_type,
        "xi-api-key": api_key
    }