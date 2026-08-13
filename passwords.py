import os
import shutil
import time
import sys
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
DATA_FILE = "passwords.txt"
RED = "\033[91m"
RESET = "\033[0m"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def loading_animation():
    terminal_width = shutil.get_terminal_size().columns
    text = "LOADING SYSTEM"
    print(RED + text.center(terminal_width) + RESET)
    
    chars = ["|", "/", "-", "\\"]
    for _ in range(3):
        for char in chars:
            sys.stdout.write(f"\r{RED}{char.center(terminal_width)}{RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    
    sys.stdout.write(f"\r{' ' * terminal_width}\r")
    sys.stdout.flush()

def print_logo():
    logo = """
██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ ███████╗
██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔════╝
██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║███████╗
██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║╚════██║
██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝███████║
╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝
    """
    terminal_width = shutil.get_terminal_size().columns
    for line in logo.splitlines():
        print(RED + line.center(terminal_width) + RESET)

def load_or_create_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    f = Fernet(key)
    return f.decrypt(data.encode()).decode()

def add_password(key):
    site = input("Enter service name: ")
    login = input("Enter username/email: ")
    password = input("Enter password: ")
    entry = f"Service: {site} | Username: {login} | Password: {password}\n"
    encrypted_entry = encrypt_data(entry, key)
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(encrypted_entry + "\n")
    print("Saved successfully!")

def view_passwords(key):
    if not os.path.exists(DATA_FILE):
        print("No saved data found.")
        return
    print("\n--- Saved Credentials ---")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            encrypted_line = line.strip()
            if encrypted_line:
                try:
                    decrypted = decrypt_data(encrypted_line, key)
                    print(f"[{i}] {decrypted.strip()}")
                except Exception:
                    print(f"[{i}] Decryption error!")

def delete_password(key):
    if not os.path.exists(DATA_FILE):
        print("No saved data found.")
        return
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    if not lines:
        print("No passwords to delete.")
        return

    print("\n--- Current Passwords ---")
    valid_entries = []
    for line in lines:
        encrypted_line = line.strip()
        if encrypted_line:
            try:
                decrypted = decrypt_data(encrypted_line, key)
                valid_entries.append(line)
                print(f"[{len(valid_entries)}] {decrypted.strip()}")
            except Exception:
                pass
                
    if not valid_entries:
        print("No valid credentials found.")
        return

    choice = input("Enter the number of the entry to delete (or 0 to cancel): ")
    try:
        idx = int(choice)
        if idx == 0:
            return
        if 1 <= idx <= len(valid_entries):
            target_line = valid_entries[idx - 1]
            lines.remove(target_line)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print("Deleted successfully!")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")

def main():
    clear_screen()
    loading_animation()
    clear_screen()
    print_logo()
    key = load_or_create_key()
    while True:
        print("\n1. Add Password")
        print("2. View Passwords")
        print("3. Delete Password")
        print("4. Exit")
        choice = input("Select choice (1-4): ")
        if choice == "1":
            add_password(key)
        elif choice == "2":
            view_passwords(key)
        elif choice == "3":
            delete_password(key)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
