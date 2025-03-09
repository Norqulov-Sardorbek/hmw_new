# Generated by Django 5.1.6 on 2025-03-08 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0002_alter_product_discount_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='order',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
