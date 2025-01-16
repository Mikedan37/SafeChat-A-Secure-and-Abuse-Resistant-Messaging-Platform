from cryptography.fernet import Fernet

# Generate and store this key securely
SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

def encrypt_message(message: str) -> str:
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(encrypted_message: str) -> str:
    return cipher.decrypt(encrypted_message.encode()).decode()