# Generated by Django 3.2.9 on 2022-01-18 21:54

from django.db import migrations, models
import django.utils.timezone
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0019_auto_20220118_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=64, verbose_name='地域')),
            ],
            options={
                'db_table': 'location',
            },
        ),
        migrations.AddField(
            model_name='userfavoriteitemmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='作成日時'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userfavoriteitemmodel',
            name='delete_flg',
            field=models.IntegerField(blank=True, default=0, verbose_name='削除フラグ'),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='id',
            field=models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='itemmodel',
            name='name',
            field=models.CharField(max_length=256, verbose_name='求人題名'),
        ),
        migrations.AlterField(
            model_name='userfavoriteitemmodel',
            name='id',
            field=models.CharField(default=ulid.api.api.Api.new, editable=False, max_length=32, primary_key=True, serialize=False),
        ),
    ]
