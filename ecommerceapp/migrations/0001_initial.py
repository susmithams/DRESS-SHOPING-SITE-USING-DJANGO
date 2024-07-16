# Generated by Django 5.0.4 on 2024-04-17 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ecomregister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propic', models.ImageField(upload_to='images/')),
                ('fullname', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=200)),
                ('phone', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
