#!/usr/bin/env python3
"""
Sakhatype Backend API Test Suite
Tests all endpoints as specified in the review request
"""

import requests
import json
import sys
from typing import Dict, Any

# Backend URL from frontend env
BASE_URL = "http://localhost:8001"

class SakhatypeAPITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.test_username = "testuser"
        self.test_password = "test1234"
        self.results = []
        
    def log_result(self, test_name: str, success: bool, message: str, response_data: Any = None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response": response_data
        })
        
    def test_health_check(self):
        """Test GET / - health check"""
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_result("Health Check", True, f"Server is running: {data['message']}")
                    return True
                else:
                    self.log_result("Health Check", False, "Response missing 'message' field", data)
            else:
                self.log_result("Health Check", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Health Check", False, f"Connection error: {str(e)}")
        return False
        
    def test_get_words(self):
        """Test GET /api/words - should return 100 words"""
        try:
            response = requests.get(f"{self.base_url}/api/words")
            if response.status_code == 200:
                words = response.json()
                if isinstance(words, list) and len(words) == 100:
                    self.log_result("Get Words", True, f"Retrieved {len(words)} words successfully")
                    return True
                else:
                    self.log_result("Get Words", False, f"Expected 100 words, got {len(words) if isinstance(words, list) else 'non-list'}", words[:5] if isinstance(words, list) else words)
            else:
                self.log_result("Get Words", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Get Words", False, f"Request error: {str(e)}")
        return False
        
    def test_register(self):
        """Test POST /api/auth/register"""
        try:
            # First, try to register a new user
            payload = {
                "username": self.test_username,
                "password": self.test_password
            }
            response = requests.post(f"{self.base_url}/api/auth/register", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "username" in data and data["username"] == self.test_username:
                    self.log_result("User Registration", True, f"User '{self.test_username}' registered successfully")
                    return True
                else:
                    self.log_result("User Registration", False, "Registration response missing username", data)
            elif response.status_code == 400 and "already exists" in response.text:
                self.log_result("User Registration", True, f"User '{self.test_username}' already exists (expected)")
                return True
            else:
                self.log_result("User Registration", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("User Registration", False, f"Request error: {str(e)}")
        return False
        
    def test_login(self):
        """Test POST /api/auth/login - using form-data"""
        try:
            # Use form data as specified
            form_data = {
                "username": self.test_username,
                "password": self.test_password
            }
            response = requests.post(
                f"{self.base_url}/api/auth/login", 
                data=form_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.token = data["access_token"]
                    self.log_result("User Login", True, f"Login successful, token received")
                    return True
                else:
                    self.log_result("User Login", False, "Login response missing token fields", data)
            else:
                self.log_result("User Login", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("User Login", False, f"Request error: {str(e)}")
        return False
        
    def test_get_current_user(self):
        """Test GET /api/users/me - with token"""
        if not self.token:
            self.log_result("Get Current User", False, "No token available (login failed)")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.base_url}/api/users/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "username" in data and data["username"] == self.test_username:
                    self.log_result("Get Current User", True, f"Retrieved user info for '{self.test_username}'")
                    return True
                else:
                    self.log_result("Get Current User", False, "User info response invalid", data)
            else:
                self.log_result("Get Current User", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Get Current User", False, f"Request error: {str(e)}")
        return False
        
    def test_save_result(self):
        """Test POST /api/results - save test result with token"""
        if not self.token:
            self.log_result("Save Test Result", False, "No token available (login failed)")
            return False
            
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {
                "wpm": 65.5,
                "raw_wpm": 70.2,
                "accuracy": 93.5,
                "burst_wpm": 75.0,
                "total_errors": 15,
                "time_mode": 30,
                "test_duration": 30,
                "consistency": 85.5
            }
            response = requests.post(f"{self.base_url}/api/results", json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "id" in data and "username" in data and data["username"] == self.test_username:
                    self.log_result("Save Test Result", True, f"Test result saved with ID {data['id']}")
                    return True
                else:
                    self.log_result("Save Test Result", False, "Result response invalid", data)
            else:
                self.log_result("Save Test Result", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Save Test Result", False, f"Request error: {str(e)}")
        return False
        
    def test_get_user_results(self):
        """Test GET /api/results/user/testuser"""
        try:
            response = requests.get(f"{self.base_url}/api/results/user/{self.test_username}")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Get User Results", True, f"Retrieved {len(data)} results for user '{self.test_username}'")
                    return True
                else:
                    self.log_result("Get User Results", False, "Results response not a list", data)
            else:
                self.log_result("Get User Results", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Get User Results", False, f"Request error: {str(e)}")
        return False
        
    def test_get_user_profile(self):
        """Test GET /api/profile/testuser"""
        try:
            response = requests.get(f"{self.base_url}/api/profile/{self.test_username}")
            
            if response.status_code == 200:
                data = response.json()
                if "username" in data and "total_tests" in data and "best_wpm" in data:
                    self.log_result("Get User Profile", True, f"Profile retrieved: {data['total_tests']} tests, best WPM: {data['best_wpm']}")
                    return True
                else:
                    self.log_result("Get User Profile", False, "Profile response missing required fields", data)
            else:
                self.log_result("Get User Profile", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Get User Profile", False, f"Request error: {str(e)}")
        return False
        
    def test_leaderboard_wpm(self):
        """Test GET /api/leaderboard/wpm"""
        try:
            response = requests.get(f"{self.base_url}/api/leaderboard/wpm")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Leaderboard WPM", True, f"Retrieved WPM leaderboard with {len(data)} entries")
                    return True
                else:
                    self.log_result("Leaderboard WPM", False, "Leaderboard response not a list", data)
            else:
                self.log_result("Leaderboard WPM", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Leaderboard WPM", False, f"Request error: {str(e)}")
        return False
        
    def test_leaderboard_accuracy(self):
        """Test GET /api/leaderboard/accuracy"""
        try:
            response = requests.get(f"{self.base_url}/api/leaderboard/accuracy")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_result("Leaderboard Accuracy", True, f"Retrieved accuracy leaderboard with {len(data)} entries")
                    return True
                else:
                    self.log_result("Leaderboard Accuracy", False, "Leaderboard response not a list", data)
            else:
                self.log_result("Leaderboard Accuracy", False, f"HTTP {response.status_code}", response.text)
        except Exception as e:
            self.log_result("Leaderboard Accuracy", False, f"Request error: {str(e)}")
        return False
        
    def run_all_tests(self):
        """Run all tests in sequence"""
        print(f"🚀 Starting Sakhatype API Tests")
        print(f"📍 Backend URL: {self.base_url}")
        print("=" * 60)
        
        # Test sequence as specified in review request
        tests = [
            ("1. Health Check", self.test_health_check),
            ("2. Get Words", self.test_get_words),
            ("3. User Registration", self.test_register),
            ("4. User Login", self.test_login),
            ("5. Get Current User", self.test_get_current_user),
            ("6. Save Test Result", self.test_save_result),
            ("7. Get User Results", self.test_get_user_results),
            ("8. Get User Profile", self.test_get_user_profile),
            ("9. Leaderboard WPM", self.test_leaderboard_wmp),
            ("10. Leaderboard Accuracy", self.test_leaderboard_accuracy)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 {test_name}")
            if test_func():
                passed += 1
            print("-" * 40)
            
        print(f"\n📊 Test Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
            return True
        else:
            print("⚠️  Some tests failed. Check the details above.")
            return False

def main():
    """Main test runner"""
    tester = SakhatypeAPITester()
    success = tester.run_all_tests()
    
    # Return appropriate exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()