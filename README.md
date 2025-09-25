# CS50 Network Project

Short description: A Django-based social network project inspired by CS50’s Network assignment. Users can create accounts, post content, follow others, and interact with posts.

## Features
- User registration and login
- Create, edit, and view posts
- Follow/unfollow users
- View posts from followed users
- Like and unlike posts
- Pagination for posts

## Tech Stack
- Python, Django, SQLite, HTML, CSS, JavaScript

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
python manage.py migrate
Create a superuser (optional):

bash
Copy code
python manage.py createsuperuser
Run server:

bash
Copy code
python manage.py runserver
Open browser at http://localhost:8000
