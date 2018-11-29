# Generated by Django 2.0 on 2018-11-29 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('spentat', models.CharField(max_length=40)),
                ('amount', models.IntegerField()),
                ('modeofpayment', models.CharField(max_length=20)),
                ('datespent', models.DateField(verbose_name='Date Spent')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
