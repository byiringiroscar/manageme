# Generated by Django 3.2.9 on 2021-12-13 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0002_alter_property_registration_owner_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property_registration',
            name='owner_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
