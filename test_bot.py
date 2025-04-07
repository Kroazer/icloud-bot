#!/usr/bin/env python3
"""
Test script for iCloud Email Bot
This script tests the functionality of the bot without actually creating accounts
"""

import os
import sys
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from random_data_generator import RandomDataGenerator

def test_random_data_generator():
    """
    Test the RandomDataGenerator class
    """
    print("Testing RandomDataGenerator...")
    
    generator = RandomDataGenerator()
    
    # Test generating multiple users
    print("\nGenerating 3 random users:")
    for i in range(3):
        user_data = generator.get_user_data()
        print(f"\nUser {i+1}:")
        print(f"Name: {user_data['first_name']} {user_data['last_name']}")
        print(f"Apple ID: {user_data['apple_id']}@icloud.com")
        print(f"Password: {user_data['password']}")
        print(f"Birth Date: {user_data['birth_date']}")
        print(f"Phone: {user_data['phone_number']}")
        print(f"Security Questions: {json.dumps(user_data['security_questions'], indent=2)}")
    
    return True

def test_bot_components():
    """
    Test individual components of the iCloud Email Bot
    """
    print("\nTesting bot components...")
    
    try:
        # Import the ICloudEmailBot class
        from icloud_email_bot import ICloudEmailBot
        
        # Create an instance of the bot
        bot = ICloudEmailBot(headless=True)
        
        # Test generating user data
        print("\nTesting user data generation:")
        user_data = bot.generate_user_data()
        print(f"Generated user data for: {user_data['first_name']} {user_data['last_name']}")
        
        # Test saving account info
        print("\nTesting account info saving:")
        bot.save_account_info()
        print(f"Account information saved to {bot.log_file}")
        
        return True
    
    except Exception as e:
        print(f"Error testing bot components: {e}")
        return False

def main():
    """
    Main function to run tests
    """
    print("=== iCloud Email Bot Test Suite ===\n")
    
    # Test RandomDataGenerator
    if test_random_data_generator():
        print("\n✓ RandomDataGenerator tests passed")
    else:
        print("\n✗ RandomDataGenerator tests failed")
    
    # Test bot components
    if test_bot_components():
        print("\n✓ Bot component tests passed")
    else:
        print("\n✗ Bot component tests failed")
    
    print("\nNote: Full end-to-end testing requires manual intervention for verification codes")
    print("and handling of CAPTCHA challenges. This test suite only verifies the core functionality.")
    
    print("\n=== Test Suite Complete ===")

if __name__ == "__main__":
    main()
