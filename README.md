# StoryTime

Welcome to the StoryTime project! This is a Django-based web application designed to help users improve their vocabulary and learn to read in a foreign language.

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/taylorhmorris/story-time.git
  cd story-time
  ```

2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

3. Install the dependencies:
  ```bash
  pip install -r requirements.txt
  ```

4. Apply migrations:
  ```bash
  python manage.py migrate
  ```

5. Create a superuser:
  ```bash
  python manage.py createsuperuser
  ```

6. Set up environment variables in a .env file
  ```bash
  PIXABAY_API_KEY={PIXABAY_API_KEY}
  RAPID_API_KEY={RAPID_API_KEY}
  HF_API_KEY={HUGGING_FACE_TOKEN}
  ```

7. Run the development server:
  ```bash
  python manage.py runserver
  ```

## Usage

- Access the application at `http://127.0.0.1:8000/notemaker`
- Log in with your superuser account or create a new account

## Run Tests

```bash
python manage.py test
```
