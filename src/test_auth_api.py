"""
Test script for Authentication API
Run after backend is running on port 8000
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    print("\n📝 TEST 1: Register User")
    print("-" * 50)
    
    data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test_{int(time.time())}@example.com",
        "password": "testpass123",
        "role": "analyst"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=data,
            timeout=5
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Registration successful!")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Role: {user['role']}")
            return user['username'], "testpass123"
        else:
            print(f"❌ Registration failed: {response.json()}")
            return None, None
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend on port 8000")
        print("   Start backend: python auth_backend.py")
        return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

def test_login(username, password):
    """Test user login"""
    print("\n🔓 TEST 2: Login User")
    print("-" * 50)
    
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=data,
            timeout=5
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            role = token_data['role']
            print(f"✅ Login successful!")
            print(f"   Role: {role}")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_verify_token(token):
    """Test token verification"""
    print("\n🔑 TEST 3: Verify Token")
    print("-" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/verify",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Token verified!")
            print(f"   Username: {data['username']}")
            print(f"   Role: {data['role']}")
            print(f"   Valid: {data['valid']}")
            return True
        else:
            print(f"❌ Token verification failed: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_user(token):
    """Test getting user info"""
    print("\n👤 TEST 4: Get User Info")
    print("-" * 50)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            user = response.json()
            print(f"✅ User info retrieved!")
            print(f"   ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Role: {user['role']}")
            print(f"   Created: {user['created_at']}")
            return True
        else:
            print(f"❌ Failed to get user info: {response.json()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_invalid_token():
    """Test invalid token handling"""
    print("\n❌ TEST 5: Invalid Token Handling")
    print("-" * 50)
    
    headers = {"Authorization": "Bearer invalid_token_12345"}
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/verify",
            headers=headers,
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"✅ Invalid token rejected correctly")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.json().get('detail')}")
            return True
        else:
            print(f"❌ Invalid token was accepted (security issue!)")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("🧪 AUTHENTICATION API TEST SUITE")
    print("="*50)
    
    # Test 1: Register
    username, password = test_register()
    if not username:
        print("\n❌ Cannot continue without successful registration")
        return False
    
    time.sleep(0.5)
    
    # Test 2: Login
    token = test_login(username, password)
    if not token:
        print("\n❌ Cannot continue without valid token")
        return False
    
    time.sleep(0.5)
    
    # Test 3: Verify Token
    if not test_verify_token(token):
        print("\n❌ Token verification failed")
        return False
    
    time.sleep(0.5)
    
    # Test 4: Get User Info
    if not test_get_user(token):
        print("\n❌ Get user info failed")
        return False
    
    time.sleep(0.5)
    
    # Test 5: Invalid Token
    if not test_invalid_token():
        print("\n❌ Invalid token handling failed")
        return False
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED!")
    print("="*50)
    return True

if __name__ == "__main__":
    main()