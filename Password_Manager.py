import json
import random
import string
import os
import time
from cryptography.fernet import Fernet


def x():
    time.sleep(3)
    os.system("cls")

class PasswordManager:
    def __init__(self):
        self.users = {}
        self.logged_in = False
        self.current_user = None
        self.file_name = "db.json"
        self.key = None

    def generate_password(self, length=22):
        characters = string.ascii_letters + string.digits + string.punctuation + string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase + string.hexdigits + string.octdigits + string.printable + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def save_data(self):
        encrypted_data = self.encrypt_data()
        with open(self.file_name, 'wb') as file:
            file.write(encrypted_data)

    def load_data(self):
        try:
            with open(self.file_name, 'rb') as file:
                encrypted_data = file.read()
                self.decrypt_data(encrypted_data)
        except FileNotFoundError:
            pass

    def generate_key(self):
        if not os.path.exists('key.key'):
            key = Fernet.generate_key()
            with open('key.key', 'wb') as key_file:
                key_file.write(key)

    def load_key(self):
        with open('key.key', 'rb') as key_file:
            self.key = key_file.read()

    def encrypt_data(self):
        cipher_suite = Fernet(self.key)
        cipher_text = cipher_suite.encrypt(json.dumps(self.users).encode())
        return cipher_text

    def decrypt_data(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        plain_text = cipher_suite.decrypt(encrypted_data)
        self.users = json.loads(plain_text.decode())

    def register(self):
        if self.logged_in:
            print("You are already logged in.")
            return

        username = input("Enter a username: ")
        password = input("Enter a password: ")

        if username in self.users:
            print("Username already exists. Please choose a different username.")
            x()
            return

        self.users[username] = {'password': password, 'passwords': {}}
        self.save_data()

        print("Registered successfully. You can now log in.")
        x()

    def login(self):
        if self.logged_in:
            print("You are already logged in.")
            return

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username in self.users and self.users[username]['password'] == password:
            self.logged_in = True
            self.current_user = username
            print(f"Welcome back, {username}!")
            x()
        else:
            print("Invalid username or password.")
            x()

    def add_password(self):
        if not self.logged_in:
            print("Please login first.")
            x()
            return

        website = input("Enter the website: ")
        username = input("Enter the username: ")
        password = input("Enter the password (leave blank to generate a random password): ")

        if password == "":
            password = self.generate_password()

        self.users[self.current_user]['passwords'][website] = {'username': username, 'password': password}
        self.save_data()

        print("Password added successfully.")
        x()

    def get_password(self, website):
        if self.logged_in and self.current_user in self.users and 'passwords' in self.users[self.current_user] and website in self.users[self.current_user]['passwords']:
            return self.users[self.current_user]['passwords'][website]
        else:
            return None

    def remove_password(self, website):
        if self.logged_in and self.current_user in self.users and 'passwords' in self.users[self.current_user] and website in self.users[self.current_user]['passwords']:
            del self.users[self.current_user]['passwords'][website]
            self.save_data()
            print("Password removed successfully.")
        else:
            print(f"No password found for website '{website}'.")

    def list_websites(self):
        if self.logged_in and self.current_user in self.users and 'passwords' in self.users[self.current_user]:
            return self.users[self.current_user]['passwords'].keys()
        else:
            return []

password_manager = PasswordManager()
password_manager.generate_key()
password_manager.load_key()
password_manager.load_data()

while True:
    print("\n----- Password Manager -----")
    print("1. Register")
    print("2. Login")
    print("3. Add Password")
    print("4. Get Password")
    print("5. Remove Password")
    print("6. List Websites")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        password_manager.register()
    elif choice == "2":
        password_manager.login()
    elif choice == "3":
        password_manager.add_password()
    elif choice == "4":
        website = input("Enter the website: ")
        password = password_manager.get_password(website)
        if password:
            print(f"Username: {password['username']}")
            print(f"Password: {password['password']}")
        else:
            print(f"No password found for website '{website}'.")
            x()
    elif choice == "5":
        website = input("Enter the website: ")
        password_manager.remove_password(website)
    elif choice == "6":
        websites = password_manager.list_websites()
        if websites:
            print("Websites:")
            for website in websites:
                print(website)
        else:
            print("No websites found.")
            x()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please try again.")
        x()

password_manager.save_data()


