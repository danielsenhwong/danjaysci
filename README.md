# danjaysci.com
## Setup
### Set Python version (Hostineer)

```
pyenv local 3.4.4
```

### Install Django, mysqlclient

```
pip install django mysqlclient
```

### Start Django project and enable as Passenger application

```
cd /var/www
mkdir danjaysci.com
cd danjaysci.com
django-admin startproject danjaysci
cd danjaysci/danjaysci
mkdir tmp public
```

Change interpreter location of `/usr/local/bin/django-admin`:

```
vim /usr/local/bin/django-admin
```

Modify shebang on first line to read:

```
#!/usr/bin/env python
```

Generate Passenger hook:

```
ln -s wsgi.py passenger_wsgi.py
```

Edit Passenger hook:

```
vim passenger_wsgi.py
```

Change the file to read:

```
import os, sys
sys.path.append("/var/www/danjaysci.com/danjaysci")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "danjaysci.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Modify settings.py to add `danjaysci.com` to `ALLOWED_HOSTS`:

```
vim settings.py
```

```
ALLOWED_HOSTS = ['danjaysci.com']
```

Move `SECRET_KEY` to a file inaccessible to web users, e.g. `/home/danielsenhwong/project_secrets/danjaysci_secret_key.txt`, and replace the `SECRET_KET` entry in `settings.py`:

```
with open('/home/danielsenhwong/project_secrets/danjaysci_secret_key.txt') as f:
    SECRET_KEY = f.read.strip()
```

The file should contain only the secret key text.

Similarly, set the Django project to use a MySQL database, but keep the settings in a separate file:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/home/danielsenhwong/project_secrets/danjaysci_database.cnf',
        },
    }
}
```

This file should contain the following information, formatted as shown:

```
[client]
database = dwong_<db_name>
user = dwong_<username>
password = <password>
default-character-set = utf8
```

Create the database, user, and assign appropriate privileges to the user using the Hostineer contorl panel.

### Set up addon domain (Hostineer)

Go to Hostineer control panel, DNS > Addon Domain > Add Domain.

Set path to `/var/www/danjaysci.com/danjaysci/danjaysci/public`.
