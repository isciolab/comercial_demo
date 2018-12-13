## What's this repository about?

Example created for the blog post [How to Use Django's Built-in Login System][blog-post] at [simpleisbetterthancomplex.com][blog].


## How do I run this project locally?

### 1. Clone the repository:

    git clone https://github.com/sibtc/simple-django-login.git

##
pip install django-cors-headers

##
pip install -U numpy

##
pip install matplotlib

##
pip install wordcloud

## Lo de abajo es importante para poder correr migraciones de forma mahual
    pip install sqlparse



##si aparece el siguiente error al ejecutar: pip install mysql-python connector
 mysql-python install error: Cannot open include file 'config-win.h'


### 2. Run migrations:

    python manage.py migrate

### 3. Create a user:

    python manage.py createsuperuser

### 4. Run the server:

    python manage.py runserver

### 5. And open 127.0.0.1:8000/login in your web browser.

[blog]: http://simpleisbetterthancomplex.com
[blog-post]: http://simpleisbetterthancomplex.com/tutorial/2016/06/27/how-to-use-djangos-built-in-login-system.html

#### LIbrerias necesarias
 pip3.6 install djangorestframework


### crear migraciones
python manage.py makemigrations 

#### libreria voice to text
pip install --upgrade google-cloud-speech==0.27