# API Output Examples

This document shows the actual API responses from the Employee Management System running in Docker.

## Docker Container Running

```
$ docker run -d -p 5000:5000 --name emp-api employee-management-system

$ docker logs emp-api
2025-11-25 08:11:53,300 - __main__ - INFO - Database initialized
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

---

## 1. Health Check Endpoint

**Request:**
```bash
GET http://localhost:5000/api/health
```

**Response:**
```json
{
  "message": "API is running",
  "success": true,
  "timestamp": "2025-11-25T08:12:43.492563"
}
```

---

## 2. Create Employee

**Request:**
```bash
POST http://localhost:5000/api/employees
Content-Type: application/json

{
  "first_name": "Dhanush",
  "last_name": "SM",
  "email": "dhanush@example.com",
  "department": "DevOps"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Employee created successfully",
  "data": {
    "id": 1,
    "first_name": "Dhanush",
    "last_name": "SM",
    "email": "dhanush@example.com",
    "department": "DevOps",
    "is_active": true,
    "created_at": "2025-11-25T08:14:37.193475"
  }
}
```

---

## 3. Get All Employees

**Request:**
```bash
GET http://localhost:5000/api/employees
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "first_name": "Dhanush",
      "last_name": "SM",
      "email": "dhanush@example.com",
      "department": "DevOps",
      "is_active": true,
      "created_at": "2025-11-25T08:14:37.193475"
    },
    {
      "id": 2,
      "first_name": "Ramesh",
      "last_name": "K",
      "email": "ramesh@yahoo.com",
      "department": "Quality",
      "is_active": true,
      "created_at": "2025-11-25T08:20:28.344591"
    }
  ],
  "pagination": {
    "page": 1,
    "pages": 1,
    "per_page": 10,
    "total": 2
  }
}
```

---

## 4. Get Single Employee

**Request:**
```bash
GET http://localhost:5000/api/employees/1
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "first_name": "Dhanush",
    "last_name": "SM",
    "email": "dhanush@example.com",
    "department": "DevOps",
    "is_active": true
  }
}
```

---

## 5. Update Employee

**Request:**
```bash
PUT http://localhost:5000/api/employees/1
Content-Type: application/json

{
  "position": "Senior DevOps Engineer",
  "salary": 85000
}
```

**Response:**
```json
{
  "success": true,
  "message": "Employee updated successfully",
  "data": {
    "id": 1,
    "first_name": "Dhanush",
    "position": "Senior DevOps Engineer",
    "salary": 85000
  }
}
```

---

## 6. Delete Employee

**Request:**
```bash
DELETE http://localhost:5000/api/employees/2
```

**Response:**
```json
{
  "success": true,
  "message": "Employee 2 deleted successfully"
}
```

---

## Docker Build Output

```
$ docker build -t employee-management-system .
[+] Building 60.8s (15/15) FINISHED
 => [internal] load build definition from Dockerfile
 => [builder 1/5] FROM docker.io/library/python:3.11-slim
 => [builder 3/5] RUN apt-get update && apt-get install -y
 => [builder 5/5] RUN pip install --no-cache-dir --user -r requirements.txt
 => exporting to image
 => => naming to docker.io/library/employee-management-system:latest
```

---

## Tech Stack Verified

- Python 3.11
- Flask 3.0.0
- SQLAlchemy 2.0.23
- Docker (Multi-stage build)
- SQLite Database

**Status: All endpoints working successfully!**
