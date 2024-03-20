import tempfile
from tkinter import *
from tkinter import messagebox
from django.conf.locale import tk
from django.shortcuts import render
import base64
import face_recognition
import cv2
import pickle
import os
import numpy as np
from pathlib import Path
from Cryptodome.Random import get_random_bytes
import glob
from pyzbar.pyzbar import decode
from Cryptodome.Cipher import AES
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_random_otp, encrypt_otp, generate_qr_code_for_encrypted_otp, decrypt_otp
import qrcode
from Cryptodome.Util.Padding import pad, unpad
import string
import random
from .models import FundTransfer
from .models import UserProfile

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def loan(request):
    return render(request, 'loans.html')

def pradhan(request):
    return render(request, 'pradhanmantriyojna.html')

def clcss(request):
    return render(request, 'clcss.html')

def Insurance(request):
    return render(request, 'Insurance.html')

def demat(request):
    return render(request, 'demat.html')

def user(request):
    return render(request, 'user.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def fundtrans(request):
    return render(request, 'fundtrans.html')

def fundform(request):
    return render(request, 'fundform.html')

def changepin(request):
    return render(request, 'changepin.html')

def admin(request):
    return render(request, 'admin.html')

def viewtrans(request):
    return render(request, 'viewtrans.html')

def generate_qr_code(otp_length, atm_pin):
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

    # Generate OTP
    otp_to_encrypt = generate_random_otp(otp_length)

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
    img.save("C:\Vaishnavi\Main\generated_qrcode.png")
    print("QR Code generated successfully.")

def my_view(request):
    if request.method == 'POST':
        print(request.POST)  # Debug print statement
        print(request.FILES)  # Debug print statement

        # Check which form was submitted
        if 'pin' in request.POST:  # ATM Pin form submitted
            atm_pin = request.POST.get('pin')
            if atm_pin:
                # Call generate_qr_code function with otp_length and atm_pin
                generate_qr_code(6, atm_pin)
                return HttpResponse("QR Code generated successfully.")
            else:
                return HttpResponse("ATM PIN is required.")
        elif 'qrFile' in request.FILES:  # QR Code upload form submitted
            qr_code = request.FILES['qrFile']
            atm_pin = request.POST.get('pin')  # Retrieve ATM PIN from the form
            if not atm_pin:
                return HttpResponse("ATM PIN is required.")
            decrypted_otp, error_message = decrypt_qr_code(qr_code, atm_pin)
            if decrypted_otp:
                return render(request, 'fundform.html', {'decryptedOTP': decrypted_otp})
            else:
                return HttpResponse("Failed to decrypt OTP from QR code.")
        else:
            return HttpResponse("Invalid form submission.")
    else:
        return render(request, 'fundform.html')
def decrypt_qr_code(file_path, atm_pin):
    try:
        # Check if ATM pin is provided
        if atm_pin is None:
            return None, "ATM PIN is required."

        # Read the image using OpenCV
        image = cv2.imread(file_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Use pyzbar to decode the QR code
        decoded_objects = decode(gray)

        # Check if any QR codes are detected
        if not decoded_objects:
            print("No QR codes found in the image.")
            return None, "No QR codes found in the image."

        # Iterate through the decoded objects
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code data: {qr_data}")

            # Assuming the QR code contains an encrypted OTP
            if qr_data.startswith('otp:'):
                encrypted_otp = qr_data[len('otp:'):]
                try:
                    # Convert ATM pin to bytes and ensure the key length is correct
                    atm_pin_bytes = atm_pin.zfill(16).encode('utf-8')

                    # Split the encrypted OTP into IV and ciphertext
                    iv, ciphertext = encrypted_otp.split(':')

                    # Decrypt the OTP using the ATM pin as the key
                    cipher = AES.new(atm_pin_bytes, AES.MODE_CBC, iv=base64.b64decode(iv))
                    decrypted_otp = unpad(cipher.decrypt(base64.b64decode(ciphertext)), AES.block_size)

                    return decrypted_otp.decode('utf-8'), None
                except Exception as e:
                    print(f"Decryption error: {e}")
                    return None, f"Decryption error: {e}"

        print("No encrypted OTP found in the QR code.")
        return None, "No encrypted OTP found in the QR code."

    except Exception as e:
        print(f"Error processing QR code: {e}")
        return None, f"Error processing QR code: {e}"



def submit(request):
    if request.method == 'POST':
        receivers_bank_name = request.POST['bankName']
        receivers_name = request.POST['receiverName']
        receivers_account_number = request.POST['accountNo']
        senders_account_number = request.POST['saccountNo']
        amount_to_transfer = request.POST['amt']
        fund_transfer_option = request.POST['option']
        date_of_transfer = request.POST['dot']
        transfer_description = request.POST['trans']

        try:
            fund_transfer = FundTransfer(
                receivers_bank_name=receivers_bank_name,
                receivers_name=receivers_name,
                receivers_account_number=receivers_account_number,
                senders_account_number=senders_account_number,
                amount_to_transfer=amount_to_transfer,
                fund_transfer_option=fund_transfer_option,
                date_of_transfer=date_of_transfer,
                transfer_description=transfer_description
            )
            fund_transfer.save()
            return HttpResponse('Data inserted successfully!')
        except Exception as e:
            print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('Invalid request method')

def subregister(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        gender = request.POST['gender']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipCode']
        account_type = request.POST['account_type']
        account_pin = request.POST['account_pin']
        verify_pin = request.POST['verify_pin']

        try:
            userprofile = UserProfile(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_no=phone,
                dob=dob,
                gender=gender,
                address=address,
                city_name=city,
                state=state,
                zip_code=zipcode,
                account_type=account_type,
                pin=account_pin
            )
            userprofile.save()
            return HttpResponse('Data inserted successfully!')
        except Exception as e:
            print(e)
            return HttpResponse(e)
    else:
        return HttpResponse('Invalid request method')



