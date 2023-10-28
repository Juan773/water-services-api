# disary_backend
### Installation

```sh
$ mkdir water-services-api && cd water-services-api
$ git clone https://gitlab.com/poker-club/water-services-api.git

####para prython con versiones menores a 4
$ virtualenv -p python virtual # or create using pycharm
$ source virtual/bin/activate
$ (virtual) cd disary_backend
$ pip install -r requieriments.txt

###Configurar Base de Datos 

```sh
$ (virtual) notepad water-services-api/config/local.cnf 
```

```
database = dysary_bd
host = localhost
user = root
port = 3306
password = 
default-character-set = utf8
```
###Migraciones [warning]
```sh
$ (virtual) python manage.py makemigrations 
$ (virtual) python manage.py migrate 
```

### Crear Super Usuario
```sh
$ (virtual) python manage.py createsuperuser 
```

### Generar archivo requirements.txt
```sh
py -m pip freeze > requirements.txt
```

### Instalar todo el archivo requirements.txt
```sh
pip install -r requirements.txt
```