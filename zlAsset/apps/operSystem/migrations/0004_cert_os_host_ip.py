# Generated by Django 2.1.5 on 2019-01-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operSystem', '0003_syncdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='cert',
            name='os_host_ip',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]