# Generated by Django 2.1.5 on 2019-02-26 19:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assure', '0006_pilot_site_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilot',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
            preserve_default=False,
        ),
    ]
