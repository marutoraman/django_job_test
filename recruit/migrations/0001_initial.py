# Generated by Django 3.2.9 on 2021-12-13 07:52

from django.db import migrations, models
import django.db.models.deletion
import ulid.api.api


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModel',
            fields=[
                ('id', models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='UserFavoriteItemModel',
            fields=[
                ('id', models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False)),
                ('item', models.ForeignKey(db_column='item_id', on_delete=django.db.models.deletion.CASCADE, to='recruit.itemmodel')),
            ],
            options={
                'db_table': 'user_favorite_item',
            },
        ),
    ]