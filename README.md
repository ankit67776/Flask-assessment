# User Management API

This project is a simple, well-structured User Management REST API built with Python and Flask. It provides endpoints for Creating, Reading, Updating, and Deleting (CRUD) user resources.

The primary goal of this project is to demonstrate a robust and maintainable system architecture, emphasizing clear boundaries, correctness, and resilience to change, built with AI-assistance.

## Key Technical Decisions

The technology and architecture were chosen to align with best practices for building scalable and maintainable web APIs.

1.  **Application Factory Pattern (`create_app`)**:
    *   **Decision**: The application is initialized within a `create_app()` function instead of being a global object.
    *   **Reasoning**: This pattern is fundamental for testability and scalability. It allows us to create multiple instances of the app with different configurations (e.g., a testing configuration with an in-memory database). This prevents common issues with global objects and circular dependencies.

2.  **Flask-RESTful for API Resources**:
    *   **Decision**: API endpoints are managed using `flask_restful.Resource` classes (`UserListResource`, `UserResource`) instead of traditional `@app.route` decorators.
    *   **Reasoning**: This enforces a clean, object-oriented structure for the API. Each resource's logic (GET, POST, PUT, DELETE) is neatly encapsulated in its own class, making the codebase more organized and easier to extend than a long file of scattered route functions.

3.  **SQLAlchemy and Flask-Migrate for Database Interaction**:
    *   **Decision**: We used `Flask-SQLAlchemy` for ORM capabilities and `Flask-Migrate` for handling database schema migrations.
    *   **Reasoning**: The ORM abstracts away raw SQL, preventing SQL injection vulnerabilities and making database interactions more Pythonic and readable. `Flask-Migrate` provides a repeatable, version-controlled way to evolve the database schema, which is critical for "Release Integrity" and preventing data loss during updates.

4.  **Marshmallow for Schema Validation and Serialization**:
    *   **Decision**: A `UserSchema` was created using `Flask-Marshmallow` to validate incoming request data and to serialize outgoing responses.
    *   **Reasoning**: This is a crucial "Interface Safety" guardrail. It ensures that no invalid data can enter our system (e.g., a malformed email address). It also separates the concerns of data shape (schema) from the data model (database), allowing them to evolve independently.

## Getting Started

### Prerequisites
*   Python 3
*   A virtual environment

### Installation & Setup

1.  **Clone the repository.**

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database:**
    The first time you run the application, the database file `project.db` will be created automatically.

### Running the Server

To start the development server, run the provided shell script:

```bash
./devserver.sh
```

The API will be available at `http://localhost:8080`.

## API Walkthrough

You can interact with the API using a tool like `curl`.

1.  **Create a new user (`POST /users`)**:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d \'\'\'{"username": "testuser", "email": "test@example.com"}\'\'\' \
    http://localhost:8080/users
    ```

2.  **Get a list of all users (`GET /users`)**:
    ```bash
    curl http://localhost:8080/users
    ```

3.  **Get a single user (`GET /users/<id>`)**:
    ```bash
    curl http://localhost:8080/users/1
    ```

4.  **Update a user (`PUT /users/<id>`)**:
    ```bash
    curl -X PUT -H "Content-Type: application/json" \
    -d \'\'\'{"username": "testuser_updated"}\'\'\' \
    http://localhost:8080/users/1
    ```

5.  **Delete a user (`DELETE /users/<id>`)**:
    ```bash
    curl -X DELETE http://localhost:8080/users/1
    ```
