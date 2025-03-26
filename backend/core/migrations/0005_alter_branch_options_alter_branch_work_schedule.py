# Generated by Django 5.1.7 on 2025-03-26 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_guide_onlineevaluationguide_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ['title'], 'verbose_name': 'Филиал', 'verbose_name_plural': 'Филиалы'},
        ),
        migrations.AlterField(
            model_name='branch',
            name='work_schedule',
            field=models.CharField(default='Круглосуточно', max_length=255, verbose_name='График работы'),
        ),
    ]
