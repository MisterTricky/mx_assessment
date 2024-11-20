# SA ID Number Validator and Holiday Checker

This Django application allows users to validate South African ID numbers and check for public holidays on their birth dates.

## Features
- SA ID number validation
- ID number information decoding (birth date, gender, citizenship)
- Public holiday checking using Calendarific API
- Search history tracking
- User-friendly interface

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root and add your Calendarific API key:
```
CALENDARIFIC_API_KEY=your_api_key_here
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure
- `id_validator/` - Main Django application
  - `models.py` - Database models for ID records and holidays
  - `views.py` - Application views and business logic
  - `forms.py` - Form validation
  - `templates/` - HTML templates
  - `static/` - CSS, JavaScript, and other static files
