# Generated by Django 4.2 on 2023-05-07 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itenspedido',
            name='observacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
