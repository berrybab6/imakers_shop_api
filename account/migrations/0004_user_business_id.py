# Generated by Django 3.2.9 on 2022-01-15 22:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20220115_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='business_id',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
