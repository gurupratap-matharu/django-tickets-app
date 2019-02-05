# Generated by Django 2.1.5 on 2019-02-05 01:57

from django.db import migrations, models
import support.models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_holiday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='day',
            field=models.DateField(help_text='Enter the date of Holiday', validators=[support.models.no_past]),
        ),
    ]
