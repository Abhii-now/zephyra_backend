# Generated by Django 5.1.5 on 2025-01-26 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mynewapp", "0002_alter_encryptedfile_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="encryptedfile",
            name="key",
            field=models.BinaryField(default=b""),
        ),
    ]
