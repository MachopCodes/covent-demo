# FastAPI with PostgreSQL Project

This project is a FastAPI application connected to a PostgreSQL database. The app provides an API for managing data and can be extended with additional features.

---

## Table of Contents

1. [Requirements](#requirements)
2. [Setup Instructions](#setup-instructions)
    - [Database Setup](#database-setup)
    - [Environment Variables](#environment-variables)
3. [Running the Application](#running-the-application)
4. [Database Migrations](#database-migrations)
5. [API Documentation](#api-documentation)
6. [Project Structure](#project-structure)
7. [Troubleshooting](#troubleshooting)

---

## Requirements

- **Python 3.8+**
- **PostgreSQL**
- **Pipenv** or **pip** for dependency management
- **Uvicorn** for running the FastAPI application

---

## Setup Instructions

### Database Setup

1. **Install PostgreSQL**:
   - Ensure PostgreSQL is installed and running.

2. **Create a Database and User**:
   - Log into PostgreSQL using the `psql` CLI:
   - Create a new database and user:

3. **Test the Connection**:
   - Verify that the new user can access the database:
     ```bash
     psql -U myuser -d mydatabase -h localhost
     ```

4. **Set Up the `.env` File**:
   - Create a `.env` file in the project directory with the following content:
     ```env
     DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase
     ```

---

### Environment Variables

Ensure that the `.env` file is correctly configured with your database credentials.

---

## Running the Application

To run the FastAPI application locally, use the following command:
```bash
uvicorn app.main:app --reload
```
---

## Testing 

This project uses pytest for testing and pytest-cov for generating test coverage reports. Follow the steps below to run the tests and check the coverage:

To run the tests, use the following command:

```bash
pytest
```

### Running Tests With Coverage

```bash
pytest --cov=app --cov-report=term
```