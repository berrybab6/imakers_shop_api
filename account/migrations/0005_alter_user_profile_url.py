# Generated by Django 3.2.9 on 2022-01-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_user_business_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_url',
            field=models.ImageField(blank=True, null=True, upload_to='users'),
        ),
    ]