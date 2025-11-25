# API Output Examples

This document shows the actual API responses from the Employee Management System running in Docker.

---

## Screenshots

### Health Check API Response


> **Drag and drop your Health Check screenshot here (Win+Shift+S to capture)**



> **Browser URL:** `http://localhost:5000/api/health`


> **Drag and drop your Get Employees screenshot here**


### Get All Employees Response  
![Employees List](https://github.com/user-attachments/assets/employees-placeholder)

> **Browser URL:** `http://localhost:5000/api/employees`

---

## 1. Docker Container Running

```bash
$ docker run -d -p 5000:5000 --name emp-api employee-management-system

$ docker logs emp-api
2025-11-25 08:11:53,300 - __main__ - INFO - Database initialized
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

---

## 2. Health Check Endpoint

**Request:**
```
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

## 3. Create Employee

**Request:**
```
POST http://localhost:5000/api/employees
Content-Type: application/json

{
  "first_name": "Dhanush",
  "last_name": "SM",
  "email": "dhanush@example.com",
  "department": "DevOps"
}
```

**Response (201 Created):**
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

## 4. Get All Employees

**Request:**
```
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
      "is_active": true
    },
    {
      "id": 2,
      "first_name": "Ramesh",
      "last_name": "K",
      "email": "ramesh@yahoo.com",
      "department": "Quality",
      "is_active": true
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

## 5. Get Single Employee

**Request:**
```
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

## 6. Update Employee

**Request:**
```
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

## 7. Delete Employee

**Request:**
```
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

```bash
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

| Component | Version |
|-----------|--------|
| Python | 3.11 |
| Flask | 3.0.0 |
| SQLAlchemy | 2.0.23 |
| Docker | Multi-stage build |
| Database | SQLite |

---

**Status: All API endpoints tested and working successfully!**
