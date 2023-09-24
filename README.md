# Todo App Backend FastAPI

This is a backend implementation of a Todo App using FastAPI. It provides RESTful API endpoints for managing user authentication, creating, reading, updating, and deleting todos. The app includes features for user authentication, role-based authorization, and password change functionality.

## Features

- **User Authentication**: Users can register, log in, and obtain access tokens for secure API access.
- **Role-Based Authorization**: The app supports two user roles: "admin" and "user". Admin users have additional privileges, such as managing all todos.
- **Todo Management**: Users can create, read, update, and delete their own todos.
- **Password Change**: Users can change their passwords securely.
- **Data Persistence**: Todos and user data are stored in a SQLite database.
- **Validation**: API requests are validated using Pydantic models, ensuring data integrity.

## Installation
1. Clone the repository:
git clone https://github.com/your-username/Todo_App_Backend_FastAPI.git

cd Todo_App_Backend_FastAPI

3. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

4. Install the required dependencies:
pip install -r requirements.txt

5. Start the FastAPI server:
uvicorn main:app --reload

## API Endpoints
User Registration: POST /auth/

- Register a new user.
- Required fields: username, first_name, last_name, password, role.

User Login: POST /auth/token

- Obtain an access token for authentication.
- Required fields: username, password.

Get User Info: GET /user/

- Get user information.
- Requires authentication.

Change Password: PUT /user/password

- Change user password.
- Requires authentication.
- Fields: password, new_password.

List All Todos: GET /todos/

- Get a list of all user-specific todos.
- Requires authentication.

Create Todo: POST /todos/todo

- Create a new todo.
- Fields: title, description, priority, complete.
- Requires authentication.

Get Todo: GET /todos/todo/{todo_id}

- Get details of a specific todo by ID.
- Requires authentication.

Update Todo: PUT /todos/todo/{todo_id}

- Update a specific todo by ID.
- Fields: title, description, priority, complete.
- Requires authentication.

Delete Todo: DELETE /todos/todo/{todo_id}

- Delete a specific todo by ID.
- Requires authentication.

Admin List Todos: GET /admin/todo

- Get a list of all todos (admin-only).
- Requires admin authentication.

Admin Delete Todo: DELETE /admin/todo/{todo_id}

- Delete a specific todo by ID (admin-only).
- Requires admin authentication.

## Authentication and Authorization
- Authentication is done using JWT (JSON Web Tokens). To obtain an access token, send a POST request to /auth/token with your username and password.

- Authorization is role-based. Regular users have the "user" role, while administrators have the "admin" role. Admins have access to additional admin-specific endpoints.

## Database
- The app uses an SQLite database to store user and todo data. The database file is todosapp.sqlite.

## Pydantic Models
- Pydantic models are used for request and response validation to ensure data integrity and security.

## Security
- Passwords are hashed using bcrypt for security.

## Dependencies
- FastAPI: Web framework for building APIs.
- SQLAlchemy: Database toolkit and ORM.
- Pydantic: Data validation and parsing using Python type annotations.
- Passlib: Password hashing library.
- Uvicorn: ASGI server for running FastAPI applications.

## Deployment
You can deploy this FastAPI app to a production environment using ASGI servers like Gunicorn and a reverse proxy server like Nginx or Apache. Ensure that you set up secure environment variables for your secret keys and database connection.

## Contributing
Feel free to contribute to this project by creating issues, suggesting enhancements, or submitting pull requests.
