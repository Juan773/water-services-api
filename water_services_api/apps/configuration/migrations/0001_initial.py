# Generated by Django 4.2.2 on 2023-11-01 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClientType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de cliente',
                'verbose_name_plural': 'Tipos de clientes',
                'permissions': (('view_clienttype', 'Listar Tipos de clientes'), ('add_clienttype', 'Agregar Tipos de clientes'), ('update_clienttype', 'Actualizar Tipos de clientes'), ('delete_clienttype', 'Eliminar Tipos de clientes')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('name', models.CharField(max_length=120, unique=True)),
                ('abbreviation', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_code', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'Pais',
                'verbose_name_plural': 'Paises',
                'permissions': (('view_country', 'Listado de paises'), ('add_country', 'Agregar paises'), ('update_country', 'Actualizar paises'), ('delete_country', 'Eliminar paises')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=60)),
                ('code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('pattern', models.CharField(blank=True, max_length=60, null=True)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Tipo de Documento',
                'verbose_name_plural': 'Tipos de documentos',
                'permissions': (('view_documenttype', 'Listar Tipos de documentos'), ('add_documenttype', 'Agregar Tipos de documentos'), ('update_documenttype', 'Actualizar Tipos de documentos'), ('delete_documenttype', 'Eliminar Tipos de documentos')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                'verbose_name': 'Metodo de pago',
                'verbose_name_plural': 'Metodos de pago',
                'permissions': (('view_paymentmethod', 'Listar Metodos de pago'), ('add_paymentmethod', 'Agregar Metodos de pago'), ('update_paymentmethod', 'Actualizar Metodos de pago'), ('delete_paymentmethod', 'Eliminar Metodos de pago')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Situation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(blank=True, max_length=6, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Situacion',
                'verbose_name_plural': 'Situaciones',
                'permissions': (('view_situation', 'Listar Situaciones'), ('add_situation', 'Agregar Situaciones'), ('update_situation', 'Actualizar Situaciones'), ('delete_situation', 'Eliminar Situaciones')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UbigeoType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('code', models.CharField(max_length=8, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('plural_name', models.CharField(max_length=60)),
                ('order', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Tipo Ubigeo',
                'verbose_name_plural': 'Tipos de Ubigeos',
                'permissions': (('view_ubigeotype', 'Listar Tipos de Ubigeos'), ('add_ubigeotype', 'Agregar Tipos de Ubigeos'), ('update_ubigeotype', 'Actualizar Tipos de Ubigeos'), ('delete_ubigeotype', 'Eliminar Tipos de Ubigeos')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Ubigeo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(max_length=70)),
                ('phone_code', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='country_ubigeo', to='configuration.country')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='parent_ubigeo', to='configuration.ubigeo')),
                ('ubigeo_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ubigeo_type_ubigeo', to='configuration.ubigeotype')),
            ],
            options={
                'verbose_name': 'Ubigeo',
                'verbose_name_plural': 'Ubigeos',
                'permissions': (('view_ubigeo', 'Listado de ubigeos'), ('add_ubigeo', 'Agregar ubigeos'), ('update_ubigeo', 'Actualizar ubigeos'), ('delete_ubigeo', 'Eliminar ubigeos')),
                'default_permissions': (),
                'unique_together': {('country', 'name', 'ubigeo_type', 'parent')},
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('document_number', models.CharField(max_length=20)),
                ('phone_code', models.CharField(blank=True, default=51, max_length=3, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=10, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='configuration/people')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='configuration/people')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='country_person', to='configuration.country')),
                ('document_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='document_type_person', to='configuration.documenttype')),
                ('ubigeo', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ubigeo_person', to='configuration.ubigeo')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'permissions': (('view_person', 'Listar personas'), ('add_person', 'Agregar persona'), ('update_person', 'Actualizar persona'), ('delete_person', 'Eliminar persona')),
                'default_permissions': (),
            },
        ),
    ]