# Generated by Django 2.0 on 2018-12-02 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_remove_expenses_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Splitmembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memeber_splits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Splits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('datecreated', models.DateField()),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_splits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Splittransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('datespent', models.DateField()),
                ('spentat', models.TextField()),
                ('spentby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='split_spentby', to='home.Splits')),
                ('spentfor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='split_spentfor', to='home.Splits')),
                ('splitid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='split_transactions', to='home.Splits')),
            ],
        ),
        migrations.AddField(
            model_name='splitmembers',
            name='splitid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Split_members', to='home.Splits'),
        ),
    ]
