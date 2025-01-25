from base64 import b64encode
import os
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .authentication import RequestToken, authorized

# Create your views here.


@api_view(['GET'])
@authorized
def my_view(request: HttpRequest, token: RequestToken) -> JsonResponse:
    return JsonResponse({'message': 'Hello, world!,',  "token": token.dict(),})

@api_view(['GET'])
def generate_aes_key(request):
    key = os.urandom(32)  # Generate a random 256-bit key
    return JsonResponse({'key': b64encode(key).decode('utf-8')})
