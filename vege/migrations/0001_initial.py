# Generated by Django 5.1.4 on 2025-01-05 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='recepies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recepie_name', models.CharField(max_length=100)),
                ('recepie_description', models.TextField()),
                ('recepie_img', models.ImageField(upload_to='CarImages/')),
            ],
        ),
    ]
