# Generated by Django 5.1.5 on 2025-04-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
