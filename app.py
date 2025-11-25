"""Employee Management System - Flask REST API

A backend application to manage employee records using REST APIs.
Built with Flask, SQLite, and follows best practices for error handling,
input validation, logging, and modular code structuring.
"""

import os
import logging
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    f'sqlite:///{os.path.join(basedir, "employees.db")}'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Employee Model
class Employee(db.Model):
    """Employee database model."""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50))
    position = db.Column(db.String(100))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert employee object to dictionary."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'department': self.department,
            'position': self.position,
            'salary': self.salary,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Input Validation
class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_employee_data(data, is_update=False):
    """Validate employee input data."""
    errors = []
    
    if not is_update:
        # Required fields for creation
        if not data.get('first_name'):
            errors.append('First name is required')
        if not data.get('last_name'):
            errors.append('Last name is required')
        if not data.get('email'):
            errors.append('Email is required')
    
    # Email format validation
    if 'email' in data and data['email']:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            errors.append('Invalid email format')
    
    # Salary validation
    if 'salary' in data and data['salary'] is not None:
        try:
            salary = float(data['salary'])
            if salary < 0:
                errors.append('Salary cannot be negative')
        except (ValueError, TypeError):
            errors.append('Salary must be a valid number')
    
    # Name length validation
    if data.get('first_name') and len(data['first_name']) > 50:
        errors.append('First name cannot exceed 50 characters')
    if data.get('last_name') and len(data['last_name']) > 50:
        errors.append('Last name cannot exceed 50 characters')
    
    if errors:
        raise ValidationError(errors)
    
    return True


# Error Handlers
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Handle validation errors."""
    logger.warning(f'Validation error: {error.args[0]}')
    return jsonify({
        'success': False,
        'error': 'Validation Error',
        'messages': error.args[0]
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.info(f'Resource not found: {request.url}')
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f'Internal server error: {str(error)}')
    db.session.rollback()
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    """Handle HTTP exceptions."""
    logger.warning(f'HTTP exception: {error.code} - {error.description}')
    return jsonify({
        'success': False,
        'error': error.description
    }), error.code


# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees with optional filtering and pagination."""
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filter parameters
        department = request.args.get('department')
        is_active = request.args.get('is_active')
        
        # Build query
        query = Employee.query
        
        if department:
            query = query.filter(Employee.department == department)
        if is_active is not None:
            query = query.filter(Employee.is_active == (is_active.lower() == 'true'))
        
        # Execute paginated query
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        logger.info(f'Retrieved {len(pagination.items)} employees (page {page})')
        
        return jsonify({
            'success': True,
            'data': [emp.to_dict() for emp in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        })
    except Exception as e:
        logger.error(f'Error retrieving employees: {str(e)}')
        raise


@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get a single employee by ID."""
    employee = Employee.query.get(employee_id)
    
    if not employee:
        logger.info(f'Employee {employee_id} not found')
        return jsonify({
            'success': False,
            'error': f'Employee with ID {employee_id} not found'
        }), 404
    
    logger.info(f'Retrieved employee {employee_id}')
    return jsonify({
        'success': True,
        'data': employee.to_dict()
    })


@app.route('/api/employees', methods=['POST'])
def create_employee():
    """Create a new employee."""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate input
    validate_employee_data(data)
    
    # Check for duplicate email
    if Employee.query.filter_by(email=data['email']).first():
        return jsonify({
            'success': False,
            'error': 'Email already exists'
        }), 409
    
    # Create new employee
    employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        department=data.get('department'),
        position=data.get('position'),
        salary=data.get('salary')
    )
    
    db.session.add(employee)
    db.session.commit()
    
    logger.info(f'Created employee {employee.id}')
    return jsonify({
        'success': True,
        'message': 'Employee created successfully',
        'data': employee.to_dict()
    }), 201


@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update an existing employee."""
    employee = Employee.query.get(employee_id)
    
    if not employee:
        return jsonify({
            'success': False,
            'error': f'Employee with ID {employee_id} not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Validate input
    validate_employee_data(data, is_update=True)
    
    # Check email uniqueness if being updated
    if 'email' in data and data['email'] != employee.email:
        if Employee.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 409
    
    # Update fields
    for field in ['first_name', 'last_name', 'email', 'phone', 'department', 'position', 'salary', 'is_active']:
        if field in data:
            setattr(employee, field, data[field])
    
    db.session.commit()
    
    logger.info(f'Updated employee {employee_id}')
    return jsonify({
        'success': True,
        'message': 'Employee updated successfully',
        'data': employee.to_dict()
    })


@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee."""
    employee = Employee.query.get(employee_id)
    
    if not employee:
        return jsonify({
            'success': False,
            'error': f'Employee with ID {employee_id} not found'
        }), 404
    
    db.session.delete(employee)
    db.session.commit()
    
    logger.info(f'Deleted employee {employee_id}')
    return jsonify({
        'success': True,
        'message': f'Employee {employee_id} deleted successfully'
    })


# Database initialization
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        logger.info('Database initialized')


if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
