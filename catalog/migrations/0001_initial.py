# Generated by Django 3.1.3 on 2020-11-13 00:22

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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('Name', models.CharField(max_length=100, unique=True, verbose_name='Categoria')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ('Name',),
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('Name', models.CharField(max_length=100, unique=True, verbose_name='Marca')),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'ordering': ('Name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('Name', models.CharField(max_length=100, unique=True, verbose_name='Producto')),
                ('Description', models.TextField(max_length=100, unique=True, verbose_name='Descripcion')),
                ('Cost', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Costo')),
                ('Price', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Precio')),
                ('Stock', models.IntegerField()),
                ('Availabel', models.BooleanField(default=True)),
                ('CategoryId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.category')),
                ('MarkId', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.mark')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ('Name',),
            },
        ),
    ]