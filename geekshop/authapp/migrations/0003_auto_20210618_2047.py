# Generated by Django 3.1.9 on 2021-06-18 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20210610_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]