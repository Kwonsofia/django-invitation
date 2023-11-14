# Generated by Django 4.2.6 on 2023-11-10 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_account_bride_mother_account_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='id',
        ),
        migrations.AddField(
            model_name='photo',
            name='photo_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weddingmain',
            name='is_used',
            field=models.BooleanField(default=True),
        ),
    ]