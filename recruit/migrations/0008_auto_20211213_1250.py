# Generated by Django 3.2.9 on 2021-12-13 12:50

from django.db import migrations, models
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0007_auto_20211213_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmodel',
            name='id',
            field=models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userfavoriteitemmodel',
            name='id',
            field=models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False),
        ),
    ]