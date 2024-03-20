import cv2
from pyzbar.pyzbar import decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
import base64
import string
import qrcode
import random

def generate_key():
    return get_random_bytes(16)

def generate_random_otp(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def encrypt_otp(otp, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(otp.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return f"{iv}:{ciphertext}"  # Combine IV and ciphertext with a separator

def decrypt_otp(encrypted_otp, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=base64.b64decode(encrypted_otp['iv']))
    decrypted_otp = unpad(cipher.decrypt(base64.b64decode(encrypted_otp['ciphertext'])), AES.block_size)
    return decrypted_otp.decode('utf-8')

def generate_qr_code_for_encrypted_otp(otp_to_encrypt, atm_pin, filename):
    # Convert ATM pin to bytes and ensure the key length is correct
    atm_pin_bytes = atm_pin.zfill(16).encode('utf-8')

    # Encrypt the OTP
    encrypted_otp = encrypt_otp(otp_to_encrypt, atm_pin_bytes)

    # Generate the QR code
    uri = f"otp:{encrypted_otp}"  # You can customize the URI format as needed
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)

    # Create an image
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print("QR Code generated successfully.")
