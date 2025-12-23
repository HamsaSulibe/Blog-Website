````
# Blog Project (Django + DRF + JWT)

A blog application built with Django. It includes a server-rendered web UI (Django templates) and a REST API (Django REST Framework) secured with JWT (SimpleJWT). The app supports posts, likes, and following users.

## About this project
Built during my summer internship as a training project to practice Django development (web UI + REST API), authentication (JWT), and relational data modeling (posts, likes, follows).

## Features

### Web UI (templates)
- View all posts
- Following feed (posts from users you follow)
- Create, edit, delete posts (edit/delete restricted to the author)
- Like/unlike posts
- Follow/unfollow users
- Login and signup pages

### REST API
- CRUD endpoints for: users, posts, likes, follows
- JWT auth endpoints (access/refresh)


## Main Models
- Post: author, title (optional), body, created_at (newest-first ordering)
- Like: user + post, one-like-per-user-per-post enforced
- Follow: follower + following, unique follow enforced + cannot follow yourself

## Project Structure
- `manage.py`: Django management entry point
- `blog_projec/`: project settings and main URL routing
  - `settings.py`: Django/DRF settings, JWT config, login redirect
  - `urls.py`: admin, accounts, JWT endpoints, and app routes
- `blog/`: main app
  - `models.py`: Post/Like/Follow + constraints
  - `views.py`: web views (posts, following feed, create/edit/delete, toggle like/follow, signup)
  - `views_api.py`: DRF viewsets for the API
  - `serializers.py`: DRF serializers
  - `urls.py`: routing for web/API (API router is enabled by default)
  - `exceptions.py`: custom DRF exception handler (consistent JSON error responses)
  - `templates/`: HTML templates for blog pages and auth pages

## Routing Note (important)
- Web pages exist, but `blog/urls.py` currently exposes the API router while web routes are commented out.
- `LOGIN_REDIRECT_URL` points to `blog:following`, so enable web routes (or adjust the redirect) to avoid login redirect issues.
- Recommended setup: enable web routes and mount the API under `/api/` to avoid conflicts.

## Run Locally
1) Create and activate a virtual environment

Windows (PowerShell):
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
````

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies
   Note: the included `requirements.txt` may contain a local Windows path entry, which can break installs on other machines. A clean install:

```bash
pip install -U pip
pip install Django djangorestframework djangorestframework-simplejwt
```

3. Migrate and run

```bash
python manage.py migrate
python manage.py runserver
```

Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Optional (admin):

```bash
python manage.py createsuperuser
```

## JWT Auth

Endpoints:

* `POST /api/token/` (returns access + refresh)
* `POST /api/token/refresh/` (refresh access token)

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"test\",\"password\":\"your_password\"}"
```

## API Endpoints

Depending on how routing is configured:

* If router is mounted at root: `/users/`, `/posts/`, `/likes/`, `/follows/`
* If mounted under `/api/`: `/api/users/`, `/api/posts/`, `/api/likes/`, `/api/follows/`

## Git Notes

Recommended `.gitignore`:

```gitignore
__pycache__/
*.pyc
.venv/
venv/
db.sqlite3
*.log
media/
.DS_Store
Thumbs.db
.vscode/
.idea/
```

Avoid committing `db.sqlite3` and virtual environment folders.

```
```
