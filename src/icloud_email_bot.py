#!/usr/bin/env python3
"""
iCloud Email Bot
A bot to automate the creation of iCloud email accounts using random user data
"""

import os
import sys
import json
import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import the RandomDataGenerator class
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.random_data_generator import RandomDataGenerator

class ICloudEmailBot:
    """
    Bot to automate the creation of iCloud email accounts
    """
    
    def __init__(self, headless=False, proxy=None):
        """
        Initialize the bot
        
        Args:
            headless (bool, optional): Run browser in headless mode. Defaults to False.
            proxy (str, optional): Proxy server to use. Defaults to None.
        """
        self.headless = headless
        self.proxy = proxy
        self.driver = None
        self.data_generator = RandomDataGenerator()
        self.user_data = None
        self.created_accounts = []
        self.log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                    "accounts.json")
    
    def setup_driver(self):
        """
        Set up the Selenium WebDriver
        """
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Add proxy if specified
        if self.proxy:
            chrome_options.add_argument(f'--proxy-server={self.proxy}')
        
        # Set up user agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        chrome_options.add_argument(f'--user-agent={user_agent}')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            return True
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            return False
    
    def generate_user_data(self):
        """
        Generate random user data for account creation
        """
        self.user_data = self.data_generator.get_user_data()
        return self.user_data
    
    def navigate_to_signup_page(self):
        """
        Navigate to the Apple ID signup page
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.driver.get("https://appleid.apple.com/account")
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "create-link"))
            )
            
            # Click on "Create Your Apple ID" link
            create_link = self.driver.find_element(By.ID, "create-link")
            create_link.click()
            
            # Wait for the signup form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "firstNameInput"))
            )
            
            return True
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error navigating to signup page: {e}")
            return False
    
    def fill_signup_form(self):
        """
        Fill out the Apple ID signup form
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Fill in first name
            first_name_input = self.driver.find_element(By.ID, "firstNameInput")
            first_name_input.send_keys(self.user_data["first_name"])
            
            # Fill in last name
            last_name_input = self.driver.find_element(By.ID, "lastNameInput")
            last_name_input.send_keys(self.user_data["last_name"])
            
            # Fill in birth date
            self.driver.find_element(By.ID, "birthMonthField").send_keys(str(self.user_data["birth_month"]))
            self.driver.find_element(By.ID, "birthDayField").send_keys(str(self.user_data["birth_day"]))
            self.driver.find_element(By.ID, "birthYearField").send_keys(str(self.user_data["birth_year"]))
            
            # Fill in email (Apple ID)
            email_input = self.driver.find_element(By.ID, "emailInput")
            apple_id = f"{self.user_data['apple_id']}@icloud.com"
            email_input.send_keys(apple_id)
            
            # Fill in password
            password_input = self.driver.find_element(By.ID, "passwordInput")
            password_input.send_keys(self.user_data["password"])
            
            # Confirm password
            confirm_password_input = self.driver.find_element(By.ID, "confirmPasswordInput")
            confirm_password_input.send_keys(self.user_data["password"])
            
            # Fill in phone number
            phone_input = self.driver.find_element(By.ID, "phoneNumberInput")
            phone_input.send_keys(self.user_data["phone_number"])
            
            # Submit the form
            continue_button = self.driver.find_element(By.ID, "continueButton")
            continue_button.click()
            
            return True
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error filling signup form: {e}")
            return False
    
    def handle_verification_code(self):
        """
        Handle the verification code step
        
        Note: This is a placeholder as verification codes typically require manual intervention
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Wait for the verification code input field
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "codeInput"))
            )
            
            print("\n==== MANUAL INTERVENTION REQUIRED ====")
            print("A verification code has been sent to the provided phone number.")
            verification_code = input("Please enter the verification code: ")
            
            # Enter the verification code
            code_input = self.driver.find_element(By.ID, "codeInput")
            code_input.send_keys(verification_code)
            
            # Click continue
            continue_button = self.driver.find_element(By.ID, "continueButton")
            continue_button.click()
            
            return True
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error handling verification code: {e}")
            return False
    
    def answer_security_questions(self):
        """
        Answer security questions
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Wait for security questions to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "security-question"))
            )
            
            # Get all security question dropdowns and answer fields
            question_dropdowns = self.driver.find_elements(By.CLASS_NAME, "security-question-dropdown")
            answer_inputs = self.driver.find_elements(By.CLASS_NAME, "security-answer-input")
            
            # Select questions and provide answers
            security_answers = [
                self.user_data["security_questions"]["pet_name"],
                self.user_data["security_questions"]["first_city"],
                self.user_data["security_questions"]["teacher"]
            ]
            
            # Select different questions for each dropdown
            for i, dropdown in enumerate(question_dropdowns):
                dropdown.click()
                time.sleep(1)
                # Select a question (different index for each dropdown)
                question_options = self.driver.find_elements(By.CLASS_NAME, "question-option")
                question_options[i + 1].click()
                
                # Fill in the answer
                answer_inputs[i].send_keys(security_answers[i])
            
            # Click continue
            continue_button = self.driver.find_element(By.ID, "continueButton")
            continue_button.click()
            
            return True
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error answering security questions: {e}")
            return False
    
    def agree_to_terms(self):
        """
        Agree to Apple's terms and conditions
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Wait for terms and conditions page
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "termsAndConditionsAccepted"))
            )
            
            # Check the agreement checkbox
            agreement_checkbox = self.driver.find_element(By.ID, "termsAndConditionsAccepted")
            agreement_checkbox.click()
            
            # Click continue
            continue_button = self.driver.find_element(By.ID, "continueButton")
            continue_button.click()
            
            return True
        
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error agreeing to terms: {e}")
            return False
    
    def save_account_info(self):
        """
        Save the created account information to a file
        """
        account_info = {
            "apple_id": f"{self.user_data['apple_id']}@icloud.com",
            "password": self.user_data["password"],
            "first_name": self.user_data["first_name"],
            "last_name": self.user_data["last_name"],
            "birth_date": self.user_data["birth_date"],
            "phone_number": self.user_data["phone_number"],
            "security_questions": self.user_data["security_questions"],
            "creation_date": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.created_accounts.append(account_info)
        
        # Save to file
        try:
            # Load existing accounts if file exists
            existing_accounts = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    existing_accounts = json.load(f)
            
            # Append new account
            existing_accounts.append(account_info)
            
            # Write back to file
            with open(self.log_file, 'w') as f:
                json.dump(existing_accounts, f, indent=2)
            
            print(f"Account information saved to {self.log_file}")
            
        except Exception as e:
            print(f"Error saving account information: {e}")
    
    def create_account(self):
        """
        Create an iCloud email account
        
        Returns:
            bool: True if successful, False otherwise
        """
        success = False
        
        try:
            # Generate random user data
            self.generate_user_data()
            
            print(f"Creating account for {self.user_data['first_name']} {self.user_data['last_name']}")
            print(f"Apple ID: {self.user_data['apple_id']}@icloud.com")
            
            # Set up the WebDriver
            if not self.setup_driver():
                return False
            
            # Navigate to the signup page
            if not self.navigate_to_signup_page():
                return False
            
            # Fill out the signup form
            if not self.fill_signup_form():
                return False
            
            # Handle verification code (requires manual intervention)
            if not self.handle_verification_code():
                return False
            
            # Answer security questions
            if not self.answer_security_questions():
                return False
            
            # Agree to terms and conditions
            if not self.agree_to_terms():
                return False
            
            # Wait for account creation confirmation
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "account-created-confirmation"))
                )
                print("Account created successfully!")
                success = True
                
                # Save account information
                self.save_account_info()
                
            except TimeoutException:
                print("Timed out waiting for account creation confirmation")
                success = False
            
        except Exception as e:
            print(f"Error creating account: {e}")
            success = False
        
        finally:
            # Close the browser
            if self.driver:
                self.driver.quit()
            
            return success
    
    def create_multiple_accounts(self, count):
        """
        Create multiple iCloud email accounts
        
        Args:
            count (int): Number of accounts to create
        
        Returns:
            int: Number of successfully created accounts
        """
        successful_count = 0
        
        for i in range(count):
            print(f"\n=== Creating account {i+1}/{count} ===")
            
            if self.create_account():
                successful_count += 1
            
            # Add a delay between account creations
            if i < count - 1:
                delay = random.randint(60, 180)  # 1-3 minutes
                print(f"Waiting {delay} seconds before creating the next account...")
                time.sleep(delay)
        
        print(f"\nCreated {successful_count} out of {count} accounts successfully")
        return successful_count

def main():
    """
    Main function to run the bot
    """
    parser = argparse.ArgumentParser(description="iCloud Email Bot")
    parser.add_argument("--count", type=int, default=1, help="Number of accounts to create")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--proxy", type=str, help="Proxy server to use (e.g., socks5://127.0.0.1:9050)")
    
    args = parser.parse_args()
    
    bot = ICloudEmailBot(headless=args.headless, proxy=args.proxy)
    bot.create_multiple_accounts(args.count)

if __name__ == "__main__":
    main()
