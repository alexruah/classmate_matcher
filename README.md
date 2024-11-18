# Personal Classmate Project

This project is a FastAPI-based server application for managing classes and students. It provides endpoints to create, read, and delete classes, as well as group students based on similarities using text embeddings.

## Features

- Create a new class
- Read details of a specific class, including its students
- List all classes with pagination
- Delete a class
- Group students based on similarities
- Additional functionalities for managing student data
- Update student embeddings when information is added or updated
- Generate groups for a class based on student embeddings

## Endpoints

### User Endpoints

- `POST /users/`: Create a new user
- `GET /users/{email}`: Read user details by email
- `PUT /users/{email}/info`: Update user information and embeddings
- `GET /users/`: List all users with pagination
- `DELETE /users/{email}`: Delete a user by email

### Class Endpoints

- `POST /classes/`: Create a new class
- `GET /classes/{class_id}`: Read class details by class ID
- `GET /classes/`: List all classes with pagination
- `DELETE /classes/{class_id}`: Delete a class by class ID

### Group Endpoints

- `GET /group/{user_id}/embeddings`: Get embeddings for a specific user
- `POST /group/groups`: Generate groups for a class based on student embeddings

### Bedrock Endpoints

- `GET /bedrock/{user_id}/embeddings`: Get embeddings for a specific user
- `POST /bedrock/groups`: Generate groups for a list of users based on their embeddings

## Usage

### Update Student Information and Embeddings

When a user adds or updates their information, the application will automatically update their embeddings.

### Generate Groups

To generate groups for a class, use the `/group/groups` endpoint. This will create groups based on the student embeddings for the specified class.