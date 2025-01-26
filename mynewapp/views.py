from base64 import b64encode
import os
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from mynewapp.models import EncryptedFile
from .authentication import RequestToken, authorized
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


# Create your views here.


@api_view(['GET'])
@authorized
def my_view(request: HttpRequest, token: RequestToken) -> JsonResponse:
    return JsonResponse({'message': 'Hello, world!,',  "token": token.dict(),})

@api_view(['GET'])
def generate_aes_key(request):
    key = os.urandom(32)  # Generate a random 256-bit key
    return JsonResponse({'key': b64encode(key).decode('utf-8')})
@api_view(['POST'])
def upload_file(request):
    key_hex = request.POST.get('key')
    iv_hex = request.POST.get('iv')
    type = request.POST.get('fileType')

    encrypted_file = request.FILES['file']

    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)

    encrypted_data = encrypted_file.read()
    tag = encrypted_data[-16:]  # Extract the last 16 bytes as the authentication tag
    ciphertext = encrypted_data[:-16]  # The rest is the ciphertext

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(ciphertext) + decryptor.finalize()
    try:
        encrypted_file_instance = EncryptedFile.objects.create(
            name=encrypted_file.name,
            iv=iv,
            tag=tag,
            key=key,
            encrypted_data=ciphertext,
            type=type
        )
        return JsonResponse({
            'status': 'success',
            'name': encrypted_file_instance.name,
            'iv': b64encode(encrypted_file_instance.iv).decode('utf-8'),
            'tag': b64encode(encrypted_file_instance.tag).decode('utf-8'),
            'uploaded_at': encrypted_file_instance.uploaded_at,
        })
    except IntegrityError:
            return JsonResponse({'status': 'error', 'message': 'A file with this name already exists'}, status=400)


@api_view(['GET'])
def fetch_encrypted_files(request):
    files = EncryptedFile.objects.all()
    files_data = [
        {
            'name': file.name,
            # 'iv': b64encode(file.iv).decode('utf-8'),
            'tag': b64encode(file.tag).decode('utf-8'),
            # 'encrypted_data': b64encode(file.encrypted_data).decode('utf-8'),
            'uploaded_at': file.uploaded_at
        }
        for file in files
    ]
    return JsonResponse({'files': files_data})

@api_view(['GET'])
def fetch_encrypted_file(request, name):
    file = get_object_or_404(EncryptedFile, name=name)
    file_data = {
        'name': file.name,
        'iv': b64encode(file.iv).decode('utf-8'),
        'tag': b64encode(file.tag).decode('utf-8'),
        'encrypted_data': b64encode(file.encrypted_data).decode('utf-8'),
        'uploaded_at': file.uploaded_at,
        'key': b64encode(file.key).decode('utf-8'),
        'type': file.type
    }
    return JsonResponse(file_data)