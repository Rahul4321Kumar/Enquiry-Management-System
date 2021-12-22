# Generated by Django 4.0 on 2021-12-21 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('enquiries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]