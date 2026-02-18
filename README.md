# Full-Stack User Management CRUD Application

This is a full-stack web application that provides complete CRUD (Create, Read, Update, Delete) functionality for managing a list of users. The project was built with a modern tech stack and developed with the assistance of an AI agent (Google Gemini) following specific engineering standards.

## Tech Stack

- **Backend**: Python with the Flask micro-framework.
  - `Flask-RESTful`: For building structured, resource-based APIs.
  - `Flask-SQLAlchemy`: For ORM-based interaction with the database.
  - `Flask-Migrate`: For handling database schema migrations.
  - `SQLite`: As the relational database.
- **Frontend**: React.
  - `axios`: For making asynchronous HTTP requests to the backend API.
- **AI-Assisted Development**: Google Gemini was used as a coding assistant.

---

## Key Technical Decisions

This section outlines the key architectural and technical decisions made during the project's development.

#### 1. Decoupled Frontend and Backend

The project is organized into two distinct directories: `api/` for the Flask backend and `frontend/` for the React application.

-   **Decision**: To build the backend as a stateless, RESTful API and the frontend as a separate single-page application (SPA).
-   **Reasoning**: This separation of concerns is a modern web development best practice. It allows the frontend and backend to be developed, deployed, and scaled independently. The API can serve various clients (web, mobile), and the frontend can be hosted on a static file server or CDN for better performance.

#### 2. Resource-Oriented API with Flask-RESTful

The backend API exposes resources (Users) and defines the operations that can be performed on them using standard HTTP methods (GET, POST, PUT, DELETE).

-   **Decision**: To use `Flask-RESTful` to structure the API.
-   **Reasoning**: `Flask-RESTful` encourages a clean, resource-oriented architecture. It simplifies routing and enforces REST principles, making the API predictable and easy to consume. We defined a `UserResource` for single-user operations and a `UserListResource` for collection-level operations.

#### 3. ORM and Schema Migrations

User data is persisted in a relational database (SQLite).

-   **Decision**: To use `Flask-SQLAlchemy` as the Object-Relational Mapper (ORM) and `Flask-Migrate` for managing database schema changes.
-   **Reasoning**: An ORM abstracts away raw SQL, reducing boilerplate code and preventing common security vulnerabilities like SQL injection. `Flask-Migrate` provides a repeatable, version-controlled way to evolve the database schema as the application's data model changes, which is essential for maintainability.


## How to Run This Project

### Prerequisites
- Python 3
- Node.js and npm

### Backend Setup
```bash
# Navigate to the api directory
cd api

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize and upgrade the database
flask db upgrade

# Run the Flask development server
flask run --port=8080
```

### Frontend Setup
```bash
# In a new terminal, navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Run the React development server
npm start
```
The application will be available at `http://localhost:3000`.
