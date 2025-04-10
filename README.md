# Countries REST API - Flask Project 

This is a full-stack Flask-based application that allows users to register, log in, generate API keys, and query information about countries using the [REST Countries API](https://restcountries.com/). 

The app also supports session management, secure API key handling, usage tracking, and comes with a polished UI and Docker support. 

--- 
## ⚙️ Tech Stack 
- **Backend**: Flask (Python) 
- **Frontend**: HTML + Bootstrap 5 (Jinja2 templates) 
- **Database**: SQLite + SQLAlchemy ORM 
- **Authentication**: Flask-Login 
- **Security**: Bcrypt (for password & API key hashing) - **Containerization**: Docker 


--- 
## 📁 Project Structure 

``` countries_api/ 
countries_api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── controllers/
│   │   └── auth_controller.py
│   ├── models.py
│   ├── routes/
│   │   ├── authentication.py
│   │   └── rest_api.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   └── utils/
│       └── security.py
├── instance/
│   └── countries.db
├── requirements.txt
├── Dockerfile
├── run.py

``` 

--- 
## 🚀 Features 
- ✅ User Registration & Login (Form + JSON) 
- ✅ Input validation (email format, password strength, duplicates) 
- ✅ Passwords & API keys hashed (bcrypt) 
- ✅ Secure API Key Generation & Regeneration 
- ✅ Protected Routes via `@login_required` 
- ✅ Track API Key Usage (SQLite table) 
- ✅ Integration with REST Countries API 
- ✅ Minimalist Bootstrap UI 
- ✅ Dockerized for production setup 


--- 
## 🔐 Security 
- Passwords are hashed with **bcrypt** before storage. 
- API keys are generated securely using `secrets.token_hex(32)` and also hashed. 
- API key validation compares hashed versions using `bcrypt.checkpw()`. 
- Flask sessions used for login state, protected with `Flask-Login`. 
- Input validation and regex checks on both frontend and backend. 

--- 
## 📦 Setup Instructions 

### 🧑‍💻 Local Setup 

- git clone https://github.com/yourusername/countries-api.git
- cd countries-api 
- python -m venv venv 
- source venv/bin/activate 


--- 

### 🐳 Docker Setup 
#### Build and run: 

```docker build -t countries-api . docker run -p 5001:5000 -v $(pwd)/instance:/app/instance countries-api ``` Visit: [http://localhost:5001](http://localhost:5001) > Ensure `instance/` folder exists before running Docker to persist database 


--- 
## 🔑 API Usage 
All country endpoints require a valid API key in the header: 
``` Header: X-API-KEY: your_generated_key ``` 


--- 

### 📌 Authentication 
#### Register 
- Endpoint: POST /auth/register
- JSON Body:
    ```
    {
    "email": "user@example.com",
    "password": "password123"
    }
    ```

#### Login 
- Endpoint: POST /auth/login
- JSON Body:
    ```
    {
    "email": "user@example.com",
    "password": "password123"
    }
    ```

--- 
### 🔐 API Key Management
#### Generate Key
- Endpoint: POST /auth/generate-api-key

#### Regenerate Key
- Endpoint: POST /auth/regenerate-api-key


--- 
### 🌍 Country Endpoints

#### Get All Countries
- Endpoint: GET /api/countries
- Response:
    ```
    [
    {
        "name": "Canada",
        "currency": { "CAD": { ... } },
        "capital": "Ottawa",
        "languages": { "eng": "English", "fra": "French" },
        "flag": "https://flagcdn.com/ca.png"
    }
    ]
    ```


#### Get Country By Name
- Endpoint: GET /api/countries/<country_name>
