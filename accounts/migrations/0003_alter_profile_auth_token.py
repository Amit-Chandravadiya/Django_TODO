# Generated by Django 3.2.3 on 2021-07-11 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='auth_token',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]