from django.db import models

class FundTransfer(models.Model):
    receivers_bank_name = models.CharField(max_length=100)
    receivers_name = models.CharField(max_length=100)
    receivers_account_number = models.CharField(max_length=100)
    senders_account_number = models.CharField(max_length=100)
    amount_to_transfer = models.CharField(max_length=100)
    fund_transfer_option = models.CharField(max_length=100)
    date_of_transfer = models.CharField(max_length=100)
    transfer_description = models.TextField()

    def __str__(self):
        return f"{self.receivers_name}'s fund transfer"

class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    city_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    account_type = models.CharField(max_length=20)
    pin = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s profile"