
# LITReview Web Application

This project is a web app allowing users to review books and ask reviews about a specific book. Following other users system and a reactive dashboard are included.

## Installation

clone the project using GitHub CLI

```bash
git clone git://github.com/gichter/P9.git
```
Go to the project directory

```bash
cd P9/
```

Open a terminal in the root folder, then create a new virtual environment

```bash
python3 -m venv env
```

Activate the virtual environment
```bash
source env/bin/activate
```

Use the packet manager [pip](https://pip.pypa.io/en/stable/) to install the project dependencies

```bash
pip install -r requirements.txt
```

Apply the migrations

```bash
python manage.py migrate
```

Launch the django server

```bash
python manage.py runserver
```

Create an account and log in !

