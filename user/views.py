from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import UserProfile,Wallet
from .utils import send_wallet_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes

# Add wallet endpoint



# Register endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')
    if not name or not password or not email or not phone_number:
        return Response({'error': 'Name, password, email, and phone number are required.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=email).exists():
        return Response({'error': 'Email already exists as username.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    # Split name into first and last name
    name_parts = name.strip().split()
    first_name = name_parts[0] if len(name_parts) > 0 else ''
    last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
    user = User.objects.create_user(
        username=email,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    UserProfile.objects.create(user=user, phone_number=phone_number)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'message': 'User registered successfully.', 'token': token.key}, status=status.HTTP_201_CREATED)

# Login endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful.', 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_wallet(request):
    wallet_name = request.data.get('wallet_name')
    wallet_phrase = request.data.get('wallet_phrase')
    if not wallet_name or not wallet_phrase:
        return Response({'error': 'wallet_name and wallet_phrase are required.'}, status=status.HTTP_400_BAD_REQUEST)
    wallet = Wallet.objects.create(user=request.user, wallet_name=wallet_name, wallet_phrase=wallet_phrase)
    send_wallet_email(request.user.email, wallet_name, wallet_phrase)
    return Response({'message': 'Wallet added successfully.'}, status=status.HTTP_201_CREATED)

