# Generated by Django 2.0.5 on 2018-06-14 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='combinations',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='combinations',
            field=models.ManyToManyField(blank=True, null=True, related_name='_warehouse_combinations_+', to='warehouse.Warehouse'),
        ),
    ]
