# Generated by Django 3.2.5 on 2021-07-25 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200118_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='BillingProfile',
        ),
    ]
