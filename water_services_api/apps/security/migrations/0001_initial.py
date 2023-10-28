# Generated by Django 4.2.2 on 2023-10-28 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0017_user_date_new_change_at_user_password_change_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Plataforma',
                'verbose_name_plural': 'Plataformas',
                'permissions': (('view_platform', 'Listado de plataformas'), ('add_platform', 'Agregar plataforma'), ('update_platform', 'Actualizar plataforma'), ('delete_platform', 'Eliminar plataforma')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('expanded', models.BooleanField(default=False)),
                ('group', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('home', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(max_length=60)),
                ('plural_title', models.CharField(max_length=70)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=200, null=True)),
                ('target', models.CharField(blank=True, max_length=60, null=True)),
                ('icon', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField()),
                ('level', models.IntegerField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='security.module')),
                ('permission', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='module_permission', to='auth.permission')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='module_platform', to='security.platform')),
            ],
            options={
                'verbose_name': 'Modulo',
                'verbose_name_plural': 'Módulos',
                'permissions': (('view_module', 'Listado de módulos'), ('add_module', 'Agregar módulo'), ('update_module', 'Actualizar módulo'), ('delete_module', 'Eliminar módulo')),
                'default_permissions': (),
            },
        ),
    ]
