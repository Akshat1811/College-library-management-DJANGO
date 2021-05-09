# Generated by Django 3.2 on 2021-04-18 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller_inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_count', models.IntegerField(null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.books')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.seller')),
            ],
        ),
        migrations.CreateModel(
            name='Payment_bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('cost', models.IntegerField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.books')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.college')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.seller')),
            ],
        ),
    ]
