# Generated by Django 3.1.4 on 2021-08-22 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='type',
            new_name='transactions_type',
        ),
    ]
