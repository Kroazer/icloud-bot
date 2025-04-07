#!/usr/bin/env python3
"""
Random Data Generator for iCloud Email Bot
Uses RandomUser.me API to generate random user data
"""

import requests
import json
import random
import string
import time
from datetime import datetime, timedelta

class RandomDataGenerator:
    """
    Class to generate random user data for iCloud email registration
    """
    
    def __init__(self):
        self.api_url = "https://randomuser.me/api/"
        self.data = None
    
    def generate_random_user(self, nationality=None):
        """
        Generate random user data from RandomUser.me API
        
        Args:
            nationality (str, optional): Nationality code for the user. Defaults to None.
        
        Returns:
            dict: Dictionary containing user data
        """
        params = {
            'format': 'json',
            'inc': 'name,gender,dob,location,email,phone,cell,picture',
            'nat': nationality if nationality else 'us,gb,ca,au'
        }
        
        try:
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                self.data = data['results'][0]
                return self.data
            else:
                raise Exception("No user data returned from API")
        
        except Exception as e:
            print(f"Error generating random user: {e}")
            return None
    
    def generate_apple_id(self):
        """
        Generate a suitable Apple ID based on user data
        
        Returns:
            str: Generated Apple ID (email format)
        """
        if not self.data:
            self.generate_random_user()
        
        first_name = self.data['name']['first'].lower()
        last_name = self.data['name']['last'].lower()
        
        # Generate different formats of Apple ID
        formats = [
            f"{first_name}.{last_name}",
            f"{first_name}{last_name}",
            f"{first_name}{last_name}{random.randint(1, 999)}",
            f"{first_name[0]}{last_name}",
            f"{first_name}{last_name[0]}",
            f"{first_name}{random.randint(1, 999)}"
        ]
        
        apple_id = random.choice(formats)
        
        # Remove special characters
        apple_id = ''.join(c for c in apple_id if c.isalnum() or c == '.')
        
        return apple_id
    
    def generate_password(self, length=12):
        """
        Generate a strong password that meets Apple's requirements
        
        Args:
            length (int, optional): Length of password. Defaults to 12.
        
        Returns:
            str: Generated password
        """
        # Ensure password meets Apple's requirements:
        # - At least 8 characters
        # - At least one uppercase letter
        # - At least one lowercase letter
        # - At least one digit
        # - At least one special character
        
        if length < 8:
            length = 8
            
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        
        # Ensure at least one of each required character type
        password = [
            random.choice(uppercase_letters),
            random.choice(lowercase_letters),
            random.choice(digits),
            random.choice(special_chars)
        ]
        
        # Fill the rest with random characters
        all_chars = uppercase_letters + lowercase_letters + digits + special_chars
        password.extend(random.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password characters
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_birth_date(self, min_age=18, max_age=65):
        """
        Generate a random birth date
        
        Args:
            min_age (int, optional): Minimum age. Defaults to 18.
            max_age (int, optional): Maximum age. Defaults to 65.
        
        Returns:
            tuple: (birth_date_str, day, month, year)
        """
        if self.data and 'dob' in self.data:
            # Use the date from the API
            dob_str = self.data['dob']['date']
            dob = datetime.fromisoformat(dob_str.replace('Z', '+00:00'))
            
            day = dob.day
            month = dob.month
            year = dob.year
            
            # Format as MM/DD/YYYY
            birth_date_str = f"{month:02d}/{day:02d}/{year}"
            
            return birth_date_str, day, month, year
        else:
            # Generate a random date
            today = datetime.now()
            min_date = today - timedelta(days=365 * max_age)
            max_date = today - timedelta(days=365 * min_age)
            
            days_range = (max_date - min_date).days
            random_days = random.randint(0, days_range)
            random_date = min_date + timedelta(days=random_days)
            
            day = random_date.day
            month = random_date.month
            year = random_date.year
            
            # Format as MM/DD/YYYY
            birth_date_str = f"{month:02d}/{day:02d}/{year}"
            
            return birth_date_str, day, month, year
    
    def generate_security_questions(self):
        """
        Generate random answers for security questions
        
        Returns:
            dict: Dictionary with security question answers
        """
        # List of possible answers for security questions
        pet_names = ["Max", "Buddy", "Charlie", "Jack", "Cooper", "Rocky", "Bear", "Duke", "Toby", "Tucker"]
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
        teachers = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
        
        return {
            "pet_name": random.choice(pet_names),
            "first_city": random.choice(cities),
            "teacher": random.choice(teachers)
        }
    
    def generate_phone_number(self):
        """
        Generate a random phone number or use the one from API
        
        Returns:
            str: Phone number in format XXX-XXX-XXXX
        """
        if self.data and 'phone' in self.data:
            # Clean up the phone number from API
            phone = self.data['phone']
            # Remove non-digit characters
            phone = ''.join(c for c in phone if c.isdigit())
            
            # Ensure it has at least 10 digits
            if len(phone) >= 10:
                # Format as XXX-XXX-XXXX (using last 10 digits)
                phone = phone[-10:]
                return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
        
        # Generate a random US phone number
        area_code = random.randint(200, 999)
        prefix = random.randint(200, 999)
        line_number = random.randint(1000, 9999)
        
        return f"{area_code}-{prefix}-{line_number}"
    
    def get_user_data(self):
        """
        Get complete user data for iCloud registration
        
        Returns:
            dict: Complete user data
        """
        if not self.data:
            self.generate_random_user()
        
        apple_id = self.generate_apple_id()
        password = self.generate_password()
        birth_date, day, month, year = self.generate_birth_date()
        security_questions = self.generate_security_questions()
        phone_number = self.generate_phone_number()
        
        user_data = {
            "first_name": self.data['name']['first'],
            "last_name": self.data['name']['last'],
            "apple_id": apple_id,
            "password": password,
            "birth_date": birth_date,
            "birth_day": day,
            "birth_month": month,
            "birth_year": year,
            "security_questions": security_questions,
            "phone_number": phone_number,
            "gender": self.data['gender'],
            "email": self.data['email'],
            "picture": self.data['picture']['large'],
            "location": {
                "street": f"{self.data['location']['street']['number']} {self.data['location']['street']['name']}",
                "city": self.data['location']['city'],
                "state": self.data['location']['state'],
                "country": self.data['location']['country'],
                "postcode": self.data['location']['postcode']
            }
        }
        
        return user_data

# Example usage
if __name__ == "__main__":
    generator = RandomDataGenerator()
    user_data = generator.get_user_data()
    print(json.dumps(user_data, indent=2))
