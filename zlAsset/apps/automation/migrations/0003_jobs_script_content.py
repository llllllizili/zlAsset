# Generated by Django 2.1.5 on 2019-03-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0002_auto_20190224_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='script_content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
