# Employee Management System

A Flask-based REST API for managing employee records with CRUD operations, SQLite database, Docker containerization, and Azure deployment ready.

## Features

- **RESTful API**: Full CRUD operations for employee management
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Proper error responses with logging
- **Database**: SQLite with SQLAlchemy ORM
- **Testing**: Unit tests with pytest
- **Containerization**: Docker support with multi-stage build
- **Azure Ready**: Configured for Azure App Service deployment

## Tech Stack

- Python 3.11
- Flask 3.0
- SQLAlchemy
- SQLite
- Docker
- pytest
- Azure App Service

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/employees` | Get all employees |
| GET | `/api/employees/<id>` | Get employee by ID |
| POST | `/api/employees` | Create new employee |
| PUT | `/api/employees/<id>` | Update employee |
| DELETE | `/api/employees/<id>` | Delete employee |

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Dhanushgowda10/employee-management-system.git
cd employee-management-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Using Docker

```bash
# Build the image
docker build -t employee-management-system .

# Run the container
docker run -p 5000:5000 employee-management-system
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

## API Usage Examples

### Create Employee
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com"}'
```

### Get All Employees
```bash
curl http://localhost:5000/api/employees
```

## Project Structure

```
employee-management-system/
├── app.py              # Main Flask application
├── test_app.py         # Unit tests
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

## Author

Dhanush S M

## License

This project is open source and available for learning purposes.


## Screenshots
<img width="1920" height="1020" alt="Screenshot 2025-11-25 140424" src="https://github.com/user-attachments/assets/f65bbd51-85e0-4e47-b965-bab5a7fbf744" />

### API Health Check Response
```json
{"message":"API is running","success":true,"timestamp":"2025-11-25T08:28:26.596446"}
```

### Get All Employees Response
```json
{
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
  "pagination": {"page": 1, "pages": 1, "per_page": 10, "total": 2},
  "success": true
}
```

### Docker Container Running
```
$ docker run -d -p 5000:5000 --name emp-api employee-management-system
$ docker logs emp-api

2025-11-25 08:11:53 - INFO - Database initialized
 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
```

### Docker Build Success
```
$ docker build -t employee-management-system .
[+] Building 60.8s (15/15) FINISHED
 => naming to docker.io/library/employee-management-system:latest
```

---
**All API endpoints tested and working successfully!**
