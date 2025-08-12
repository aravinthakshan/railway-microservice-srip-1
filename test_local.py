#!/usr/bin/env python3
"""
Test script to verify the Railway microservice works locally
"""

import requests
import json
import os

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root_endpoint(base_url):
    """Test the root endpoint"""
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_parser_endpoint(base_url):
    """Test the parser test endpoint"""
    try:
        response = requests.get(f"{base_url}/test-parser")
        print(f"✅ Parser test: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Parser test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Railway Microservice Locally")
    print("=" * 50)
    
    # Get base URL from environment or use default
    base_url = os.environ.get("RAILWAY_URL", "http://localhost:8000")
    print(f"Testing service at: {base_url}")
    print()
    
    tests = [
        ("Health Check", lambda: test_health_endpoint(base_url)),
        ("Root Endpoint", lambda: test_root_endpoint(base_url)),
        ("Parser Test", lambda: test_parser_endpoint(base_url)),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"--- Testing {test_name} ---")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Service is ready for Railway deployment.")
    else:
        print("💥 Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 