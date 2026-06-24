# Snippet API Django

A simple Django REST Framework API for snippet management.

## Setup

1. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run migrations:

```powershell
python manage.py migrate
```

4. (Optional) Create a superuser:

```powershell
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
```

## API

- List/create snippets: `http://127.0.0.1:8000/api/snippets/`
- Detail/update/delete snippet: `http://127.0.0.1:8000/api/snippets/<id>/`
- Search snippets: `http://127.0.0.1:8000/api/snippets/?search=keyword`

## Tests

Run the snippet tests with:

```powershell
python manage.py test snippets
```
