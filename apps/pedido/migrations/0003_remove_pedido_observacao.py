# Generated by Django 4.2 on 2023-05-07 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_itenspedido_observacao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='observacao',
        ),
    ]