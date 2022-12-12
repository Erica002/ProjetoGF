# Generated by Django 4.1.3 on 2022-12-10 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesa',
            name='forma_pagamento',
            field=models.CharField(choices=[('Cartão de Crédito', 'Cartão de Crédito'), ('Dinheiro', 'Dinheiro'), ('Pix', 'Pix')], default='Dinheiro', max_length=155),
        ),
        migrations.AddField(
            model_name='renda',
            name='origem',
            field=models.CharField(choices=[('Salário', 'Salário'), ('Freelancer', 'Freelancer'), ('Extra', 'Extra')], default='Extra', max_length=155),
        ),
    ]