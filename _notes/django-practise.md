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
- allows us to specify urls for the app, like `/polls` for example

# 04. Running the server
```Shell
python3 manage.py runserver
```



