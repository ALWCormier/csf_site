# Generated by Django 4.2.3 on 2023-07-22 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csf.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csf.category')),
                ('subcat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='csf.subcategory')),
            ],
        ),
    ]
