from django.core.management.base import BaseCommand
from mynewapp.models import EncryptedFile

class Command(BaseCommand):
    help = 'Clears all records of EncryptedFile'

    def handle(self, *args, **kwargs):
        EncryptedFile.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all EncryptedFile records'))