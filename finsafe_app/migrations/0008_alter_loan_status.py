# Generated by Django 5.1.5 on 2025-01-17 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finsafe_app', '0007_group_membership_group_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Paid', 'Paid')], max_length=10),
        ),
    ]
