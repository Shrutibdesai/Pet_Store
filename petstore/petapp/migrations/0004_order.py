# Generated by Django 5.0.7 on 2024-08-20 05:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0003_pet_petimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.IntegerField()),
                ('quantity', models.ImageField(upload_to='')),
                ('petid', models.ForeignKey(db_column='petid', on_delete=django.db.models.deletion.CASCADE, to='petapp.pet')),
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
