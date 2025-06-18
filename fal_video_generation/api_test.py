#!/usr/bin/env python3
"""
Simple API test to verify FAL AI key is working
"""

import fal_client
import os
from dotenv import load_dotenv

def test_api_key():
    """Test if the FAL API key is working"""
    # Load environment variables
    load_dotenv()
    api_key = os.getenv('FAL_KEY')
    
    print('🔑 API Key loaded:', api_key[:20] + '...' if api_key else 'None')
    
    if not api_key:
        print('❌ No API key found in .env file')
        return False
    
    # Set the API key
    fal_client.api_key = api_key
    
    try:
        print('🧪 Testing API connection...')
        
        # Test with a simple request
        result = fal_client.run(
            'fal-ai/minimax/hailuo-02/standard/image-to-video',
            arguments={
                'image_url': 'https://storage.googleapis.com/falserverless/model_tests/hailuo/hailuo_test_image.jpg',
                'prompt': 'A simple test',
                'duration': '6'
            }
        )
        
        print('✅ API key is working! Video generation successful.')
        print('📹 Video URL:', result.get('video', {}).get('url', 'Not available'))
        return True
        
    except Exception as e:
        if 'unauthorized' in str(e).lower() or 'invalid' in str(e).lower():
            print('❌ API key authentication failed:', str(e))
        else:
            print('⚠️  API key is valid, but there was an error:', str(e))
        return False

if __name__ == '__main__':
    test_api_key() 