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
