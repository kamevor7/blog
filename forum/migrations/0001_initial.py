# Generated by Django 3.1.7 on 2021-03-02 17:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_Name', models.CharField(max_length=50)),
                ('last_Name', models.CharField(max_length=50)),
                ('phone_Number', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(help_text='Enter the two letters code for your State', max_length=2)),
                ('zipcode', models.CharField(max_length=15)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
