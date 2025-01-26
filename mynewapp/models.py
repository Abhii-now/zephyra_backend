from django.db import models

#
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
class EncryptedFile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    iv = models.BinaryField()
    tag = models.BinaryField()
    encrypted_data = models.BinaryField()
    key= models.BinaryField(default=b'')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255, default='text/')
    
    def __str__(self):
        return self.name