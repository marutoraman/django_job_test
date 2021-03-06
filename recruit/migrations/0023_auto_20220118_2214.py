# Generated by Django 3.2.9 on 2022-01-18 22:14

from django.db import migrations, models
import django.db.models.deletion
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0022_auto_20220118_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemmodel',
            name='location',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='recruit.locationmodel'),
        ),
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
