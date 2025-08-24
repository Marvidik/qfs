from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} Profile"


# Create your models here.

# Wallet model
class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wallets')
    wallet_name = models.CharField(max_length=100)
    wallet_phrase = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.wallet_name} ({self.user.username})"


class UserCoin(models.Model):
    COIN_CHOICES = [
        ('BTC', 'Bitcoin'),
        ('ETH', 'Ethereum'),
        ('XRP', 'Ripple'),
        ('LTC', 'Litecoin'),
        ('XLM', 'Stellar'),
        ('DOGE', 'Doge Coin'),
        ('ALGO', 'Algorand'),
        ('SOL', 'Solana'),
        ('ADA', 'Cardano'),
        ('USDT', 'Tron (Tether)'),
        ('BUSD', 'Binance USD'),
        ('SHIB', 'Shiba Inu'),
        ('PEPU', 'PEPU'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coins')
    quantity=models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    coin_symbol = models.CharField(max_length=20, choices=COIN_CHOICES)  # restricted choices
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'coin_symbol')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.user.username} - {self.coin_symbol}: {self.amount}"

    

# UserVerification model (to handle KYC/verification status)
class UserVerification(models.Model):
    STATUS_CHOICES = (
        ('unverified', 'Unverified'),
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='verification')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unverified')
    verified_at = models.DateTimeField(null=True, blank=True)
    document = models.FileField(upload_to='kyc_documents/', null=True, blank=True)  # optional KYC docs
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"