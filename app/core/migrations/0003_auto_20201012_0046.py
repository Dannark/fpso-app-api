# Generated by Django 2.1.15 on 2020-10-12 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201011_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='status',
            field=models.BooleanField(default='active', max_length=200),
        ),
    ]
