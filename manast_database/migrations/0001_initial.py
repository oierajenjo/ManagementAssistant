# Generated by Django 2.2 on 2020-06-10 21:01

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manast_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='name_category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='name_item')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='manast_database.Category', verbose_name='category_item')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manast_site.Shop')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=4, default=1.0, max_digits=10, verbose_name='quantity_sale')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='price_sale')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='cost_sale')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date_sale')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manast_database.Item', verbose_name='item_sale')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manast_site.Shop')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, default=1.0, max_digits=10, verbose_name='quantity_expense')),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='cost_expense')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date_exp')),
                ('periodicity', models.IntegerField(default=1, verbose_name=[(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly '), (4, 'Annual')])),
                ('repeat', models.BooleanField(default=False, verbose_name='repeat_expense')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manast_database.Item', verbose_name='item_exp')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manast_site.Shop')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
            },
        ),
    ]