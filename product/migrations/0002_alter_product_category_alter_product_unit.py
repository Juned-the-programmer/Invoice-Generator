# Generated by Django 5.1.4 on 2025-01-12 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Candy', 'Candy'), ('Cup', 'Cup'), ('Cone', 'Cone')], default='other', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('Box', 'Box')], default='piece', max_length=10),
        ),
    ]
