# StarPluss Fitness Studio API

A RESTful API built with **FastAPI, Python, and PostgreSQL** for managing fitness classes, user authentication, and class bookings.

## Features

- User registration and login
- JWT-based authentication
- Secure password hashing
- Create and view upcoming fitness classes
- Book fitness classes with slot availability validation
- Prevent duplicate bookings and overbooking
- View bookings belonging to the authenticated user
- IST timezone support for class schedules
- Input validation and structured error responses
- Automatic API documentation with Swagger UI
- Unit tests for input validation

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Password Hashing:** Argon2
- **Validation:** Pydantic
- **Testing:** Pytest
- **API Documentation:** Swagger UI

## Project Structure

```text
starpluss/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── routes.py
│   └── logging_config.py
├── tests/
│   └── test_schemas.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or later
- PostgreSQL
- pip

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd starpluss
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

Create a database named:

```text
starpluss_db
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/starpluss_db
SECRET_KEY=YOUR_RANDOM_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the example password and secret with your own values. Never commit `.env` to GitHub.

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will run at:

http://127.0.0.1:8000

### 7. Open API documentation

Swagger UI:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/signup` | Register a user | No |
| POST | `/login` | Log in and obtain a JWT | No |
| GET | `/classes` | View upcoming classes | No |
| POST | `/classes` | Create a fitness class | Yes |
| POST | `/book` | Book a fitness class | Yes |
| GET | `/bookings` | View your bookings | Yes |
| GET | `/` | API welcome message | No |
| GET | `/health` | Health check | No |

## Sample Requests

### Register a user — POST `/signup`

```json
{
  "name": "Demo User",
  "email": "demo@example.com",
  "password": "DemoPass123"
}
```

### Log in — POST `/login`

```json
{
  "email": "demo@example.com",
  "password": "DemoPass123"
}
```

The response includes an `access_token`. Use it to authorize protected endpoints.

### Create a fitness class — POST `/classes`

```json
{
  "name": "Yoga",
  "dateTime": "2026-12-15T09:00:00+05:30",
  "instructor": "Anita Sharma",
  "availableSlots": 20
}
```

Requires authentication.

### Book a class — POST `/book`

```json
{
  "class_id": 1,
  "client_name": "Demo User",
  "client_email": "demo@example.com"
}
```

Requires authentication. The class ID must belong to an existing, upcoming class with available slots.

### View upcoming classes — GET `/classes`

Returns upcoming fitness classes with their schedules displayed in IST.

### View your bookings — GET `/bookings`

Returns bookings associated with the authenticated user.

## Authentication

The API uses JSON Web Tokens (JWT).

1. Register using `/signup`.
2. Log in using `/login`.
3. Copy the returned `access_token`.
4. Click **Authorize** in Swagger UI.
5. Enter the token as a Bearer token if prompted, then authorize.
6. Use protected endpoints.

Tokens expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`.

## Running Tests

Run the schema validation tests from the project root:

```bash
python -m pytest tests/test_schemas.py -v
```

## Error Handling and Validation

The API validates incoming request data and handles common errors, including invalid input, invalid credentials, missing classes, duplicate bookings, and unavailable class slots.

## License

This project was developed as a fitness studio booking API assignment.
## Sample Input Data

The `sample_data.json` file contains example request bodies for:
- User registration
- User login
- Creating a fitness class
- Booking a fitness class

Use these examples in Swagger UI at `/docs` or in Postman.
The demo user must be registered before login, and a class
must exist before booking.