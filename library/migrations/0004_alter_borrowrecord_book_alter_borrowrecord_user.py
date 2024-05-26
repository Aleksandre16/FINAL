# Generated by Django 5.0.6 on 2024-05-26 18:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_rename_date_borrowed_borrowrecord_borrowed_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrecord',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_records', to='library.book'),
        ),
        migrations.AlterField(
            model_name='borrowrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='borrow_records', to=settings.AUTH_USER_MODEL),
        ),
    ]
