# Django Practise Notes
- [Django Crash Course](https://www.youtube.com/watch?v=e1IyzVyrLSU&t=3054s)


# 01. Setup

## Setup a virtual environment
```Shell
python3 -m venv 01_pollster-venv
```

## Activate the virtual environment
```Shell
source 01_pollster-venv/bin/activate
```

## To deactivate
- run when the virtual environment is active
```Shell
deactive
```

## Installing Django with Pip
```Shell
pip3 install Django
```

# 02. Django configuration
- cd into `01_pollster`
  - we can use `ls` to show the contents of the folder
- starting a new Django project
```Shell
django-admin startproject pollster
```

# 03. Folder structure

## settings.py:
- `pollster/settings.py` has all the settings for a Django project
  - in this we specify installed apps, our secret key for production and databases for example
  - we're using `sqlite3` in this project, this is the default database
    - but we can change this to postgress or mysql easily

## Hiding the secret key in an .env file
[guide](https://dev.to/earthcomfy/django-how-to-keep-secrets-safe-with-python-dotenv-5811)
- we install `dotenv` in the virtual environment
- we add a .env file in the Django root and make sure .gitignore includes it so it's not committed
- inside the file we add
```
SECRET_KEY=<the secret key>
```
- imports
``` Python pollster/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
```

## urls.py:
- allows us to specify route urls for the app, like `/polls` for example

# 04. Running the server
- by default this will run on port `8000`
```Shell
python3 manage.py runserver
```
- we now have a running server and are shown the default landing page.

# 04. Migrations
- we get a message when we run the server that we have unapplied migrations for the default tables.
  - migrations are used to give instructions to Django how to setup the database tables.

- to apply migrations we run
``` Shell
python3 manage.py migrate
``` 

# 05. Creating a Django App
- we have Django setup but we still need to create an app 
``` Shell
python3 manage.py startapp polls
```
- this creates a `polls` folder
- this includes:
  - `migrations`:
  - `admin.py`  : for if we want to make additions to the admin area. Like  `polls/questions` for example
  - `apps.py`   : we're not going to touch this
  - `models.py` : we add our database models here. we'll have a question model and a choice model.
  - `tests.py`  : we're not touching this
  - `views.py`  : can render templates, we can conntect views to urls so we can render or expose over a REST api

# 06. Adding the Question Model
- in `polls/models.py` we add a class `model` which extends `models/Model`
``` Python
class Question(models.Model):
  pass
```

## Declaring a CharField
- `CharField` is a string field for small to large sized texts 
  - more info:[page](https://www.geeksforgeeks.org/charfield-django-models/)

- we can create an instance `models.CharField` and specify a `max_length`
``` Python
question_text = models.CharField(max_length=200)
```


## Declaring a DateTimeField
- This a field in wich we can specify a date and time 
  - more info: [page](https://www.geeksforgeeks.org/datetimefield-django-models/)
- 
``` Python
pub_data = models.DateTimeField('date published')
```

# 07. Adding the Choice class

## question id reference
- for this we use a `ForeignKey`
  - we have to link to `foreign key` to a `primary key`
- we also specify an `on_delete method`
  - we set this to CASCADE so when we delete a question the choices will also get deleted.
    - this way we prevent choices from lingering that have no question assiociated with them.
``` Python 
class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)
```

# 08. Elegantly displaying fields in the admin area
- we use `__str__` to return a proper text for the fields
  - else it will display `Question Object` which looks weird

- so we add this to both classes
  - but we change `choice` to the proper word
``` Python
def __str__(self):
    return self.choice_text
```

# 09. Adding polls app to settings
- in `pollster/settings.py` we add 
``` Python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    # other apps
]
```

# 10. Creating migrations
- we need to do this to create the model instructions for the tables
```Shell
python3 manage.py makemigrations polls
````

# 09. Adding Data

## Through the shell
- left vid at 16:49







