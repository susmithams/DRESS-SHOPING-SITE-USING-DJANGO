# Generated by Django 5.0.4 on 2024-04-23 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0003_rename_fstname_ecomregister_fullname_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='sellerproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productimage', models.ImageField(upload_to='images/')),
                ('product', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('size', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=500)),
            ],
        ),
    ]
