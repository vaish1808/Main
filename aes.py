import cv2
from pyzbar.pyzbar import decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
import base64
import random
import string
import qrcode

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

def generate_qr_code_for_encrypted_otp(otp_to_encrypt, atm_pin):
    # Convert ATM pin to bytes and ensure the key length is correct
    atm_pin_bytes = atm_pin.zfill(16).encode('utf-8')

    # Encrypt the OTP
    encrypted_otp = encrypt_otp(otp_to_encrypt, atm_pin_bytes)
    print(f"Encrypted OTP: {encrypted_otp}")

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
    img.save("generated_qrcode.png")
    print("QR Code generated successfully.")


def scan_and_decrypt_qr_code(file_path, atm_pin):
    try:
        # Convert ATM pin to bytes and ensure the key length is correct
        atm_pin_bytes = atm_pin.zfill(16).encode('utf-8')

        # Read the image using OpenCV
        image = cv2.imread(file_path)

        # Check if the image is empty
        if image is None:
            raise Exception("Unable to read the image. Check the file path and file integrity.")

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use pyzbar to decode the QR code
        decoded_objects = decode(gray)

        # Check if any QR codes are detected
        if not decoded_objects:
            print("No QR codes found in the image.")
            return

        # Iterate through the decoded objects
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code data: {qr_data}")

            # Assuming the QR code contains an encrypted OTP
            if qr_data.startswith('otp:'):
                encrypted_otp = qr_data[len('otp:'):]

                # Split the encrypted OTP into IV and ciphertext
                iv, ciphertext = encrypted_otp.split(':')

                # Decrypt the OTP using the ATM pin as the key
                decrypted_otp = decrypt_otp({'iv': iv, 'ciphertext': ciphertext}, atm_pin_bytes)

                print(f"Decrypted OTP: {decrypted_otp}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Take 4-digit ATM Pin from the user
    atm_pin = input("Enter ATM Pin (4 digits): ")

    # Generate a random OTP with characters and numbers
    random_otp = generate_random_otp(8)
    print(f"Random OTP: {random_otp}")

    # Generate QR code for the encrypted OTP using the entered ATM Pin
    generate_qr_code_for_encrypted_otp(random_otp, atm_pin)

    # Scan and Decrypt QR Code
    scan_and_decrypt_qr_code("generated_qrcode.png", atm_pin)