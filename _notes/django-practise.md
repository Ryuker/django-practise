# Django Practise Notes
- [Django Crash Course](https://www.youtube.com/watch?v=e1IyzVyrLSU&t=3054s)

```Shell
python3 manage.py runserver
```

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
pub_date = models.DateTimeField('date published')
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
  - this creates a file in migrations with these instructions `00001_initial.py`
```Shell
python3 manage.py makemigrations polls
```

## Creating the tables for the models
- now we need to run `migrate` to create the tables
``` Shell
python3 manage.py migrate
```

# 11. Adding Data

## Through the shell
- we activate the shell
``` Shell
python3 manage.py shell
```
- bring in the models
``` Shell
from polls.models import Question,Choice
```
- we can then query the tables
  - this return an empty query set because we haven't added anything into the tables yet
``` Shell
Question.objects.all()
```

## Adding a question through the shell
- we import the `timezone` package from `django.utils`
  - this is need for the publish date
``` Shell
from django.utils import timezone
```
- adding the question to a variable 
  - this isn't saved in the database yet
``` Shell
q = Question(question_text="What is your favorite framework?", pub_date=timezone.now())
```
- to save it we run 
```Shell
q.save()
```

- Now it's in the database.

- We can get access fields on it using `.`
``` Shell
# example
q.question_text
```

## Filtering
- filter by ID
  - return an array
``` Shell
Question.objects.filter(id=1)
```

- filter by primary key
  - gives us a single entry
``` Shell
Question.objects.get(pk=1)
```

## Getting the choices
```Shell
# store question into `q` object
q = Question.objects.get(pk=1)
# getting the choices - will return an empty queryset for now since we have no choices yet
q.choice_set.all()
```

## Adding choices
- we use the `.create()` method for this on the `choice_set`
``` Shell
q.choice_set.create(choice_text="Django", votes=0)
q.choice_set.create(choice_text="Flask", votes=0)
q.choice_set.create(choice_text="Web2py", votes=0)
```
- we now have 3 choices in the choice_set

## Quitting the Python shell
```Shell 
quit()
```

# 12. Setting up admin user
- we need this to be able to login to our admin area
``` Shell
python3 manage.py createsuperuser
```
- we fill in user info
- and can then login at `siteurl/admin/` with the super user

# 13. Expanding the Admin Area with Questions
- we have to add these in `polls/admin.py`
- we import the models
``` Python
from .models import Question, Choice
```
- we register the Question and Choice model
``` Python
admin.site.register(Question)
admin.site.register(Choice)
```
- It now shows in the admin area.

# 14. Nesting choices under questions

## Adding ChoiceInline class
- this contains the `model` and `extra` as a field
  - extra is for extra choices, it's optional to add
- it inherits from `admin.TabularInline`
```Python
class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3
```

## Adding QuestionAdmin class
- this inherits from `admin.ModelAdmin`
- in this we set `fieldsets`
  - this is an array with two tuples
    - hence we need a trailing comma after the last tuple
- we then set inlines to the ChoiceInline class inside an array
``` Python
class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['question_text']}),
    ('Date Information', {
      'fields': ['pub_date'], 
      'classes': ['collapse']
    }),
  ]
  inlines = [ChoiceInline]
```

- We then register `Question` and `QuestionAdmin`
``` Python
admin.site.register(Question, QuestionAdmin)
```

- We now see Choices as an TabularInline panel under a specific question

# 15. Changing the site header and title
``` Python poll/admin.py
admin.site.site_header = "Pollster Admin"
admin.site.site_title = "Pollster Admin Area"
admin.site.index_title = "Welcome to the Pollster admin area"
```

# 15. Frontend polls URL
``` Python polls/views.py
from .models import Question, Choice

# Get questions and display them
def index(request):
  return render(request, 'polls/index.html')
```
- the above won't do anything yet because we don't have `index.html` yet and we haven't created the url route

## Adding URL route
- we create `polls/urls.py`
- we use the `.` symbol to import all views from all
- we specify an `app_name`
- we specify `urlpatterns` with an array
  - in this array we specify a path
    - we use `''` for the first parameter so the url remains `/polls`
    - we pass in the `index` method we created in the views file
    - we set name to `index`

``` Python polls/urls.py
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
  path('', views.index, name='index')
]
``` 

## Importing the URL into Django's urls
- we import the url in `pollster/urls.py`
``` Python pollster/urls.py
from django.urls import include, path
```
- we add the path
``` Python 
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

# 16. Adding a Template for the polls index
- to keep things organized we add `templates/polls/index.html` in the pollster root folder
- we then just add some basic html

## Pointing Django to the right templates folder
- in `pollster/settings.py` we need to specify which directory to use for the templates
- to do this we edit `DIRS` inside the `TEMPLATES` array
``` Python pollster/settings.py
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

# 17. Creating a base.html file for other templates to extend
- this way we don't need to repeat our basic header code
- we create `templates/base.html`

## Django Syntax
- using `{% //code goes here %} we can access Django properties in html

## Blocks
- we have to open and end blocks using 
  `{% block %} {% endblock %}`
  - we can name blocks
  - we name them so we can specify what goes in them in templates that extend this template

```HTML templates/base.html
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

  <title>Pollster {% block title %} {% endblock %}</title>

</head>
<body>
  <div class="container">
    <div class="row">
      <div class="col-md-6 m-auto">
        {% block content %} {% endblock %}
      </div>
    </div>
  </div>
</body>
</html>
```















