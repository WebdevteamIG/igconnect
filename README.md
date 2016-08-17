##IG-Connect 

A Django based project to connect all of the NITW students to Innovation Garage and share their projects.

##Installation and Running

Create a virtual machine:

```
    $ virtualenv env
    $ source env/bin/activate
```
Install the following : 

```
    pip install git+https://github.com/django-nonrel/django@nonrel-1.5
    pip install git+https://github.com/django-nonrel/djangotoolbox
    pip install git+https://github.com/django-nonrel/mongodb-engine
```

Run mongodb and type the following commands :

```
    $ mongo
    > use igconnect_db
    > db.createUser({user:"username", pwd:"password",roles:[]})
```

Then, edit `igconnect/settings.py` and change your username and password as you have in mongo

```
USERNAME_DB = 'username' #username for your database
PASSWORD_DB = 'password' #password for your database
```

Run server using `manage.py`
```
    ./manage.py runserver
```