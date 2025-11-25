"""Unit tests for Employee Management System API.

This module contains comprehensive tests for all CRUD operations,
input validation, and error handling.
"""

import pytest
import json
from app import app, db, Employee


@pytest.fixture
def client():
    """Create test client and initialize test database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


@pytest.fixture
def sample_employee():
    """Return sample employee data."""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'department': 'Engineering',
        'position': 'Software Developer',
        'salary': 75000.00
    }


class TestHealthCheck:
    """Tests for health check endpoint."""
    
    def test_health_check(self, client):
        """Test API health check endpoint."""
        response = client.get('/api/health')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['message'] == 'API is running'


class TestCreateEmployee:
    """Tests for employee creation endpoint."""
    
    def test_create_employee_success(self, client, sample_employee):
        """Test successful employee creation."""
        response = client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 201
        assert data['success'] is True
        assert data['data']['first_name'] == 'John'
        assert data['data']['email'] == 'john.doe@example.com'
    
    def test_create_employee_missing_required_fields(self, client):
        """Test employee creation with missing required fields."""
        response = client.post(
            '/api/employees',
            data=json.dumps({'first_name': 'John'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert data['success'] is False
    
    def test_create_employee_invalid_email(self, client):
        """Test employee creation with invalid email format."""
        employee_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email'
        }
        response = client.post(
            '/api/employees',
            data=json.dumps(employee_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert data['success'] is False
    
    def test_create_employee_duplicate_email(self, client, sample_employee):
        """Test employee creation with duplicate email."""
        # Create first employee
        client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        # Try to create duplicate
        response = client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 409
        assert 'already exists' in data['error']


class TestGetEmployees:
    """Tests for retrieving employees."""
    
    def test_get_all_employees_empty(self, client):
        """Test getting all employees when database is empty."""
        response = client.get('/api/employees')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        assert data['data'] == []
    
    def test_get_all_employees(self, client, sample_employee):
        """Test getting all employees."""
        # Create an employee first
        client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        
        response = client.get('/api/employees')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert len(data['data']) == 1
    
    def test_get_employee_by_id(self, client, sample_employee):
        """Test getting a single employee by ID."""
        # Create an employee
        create_response = client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        employee_id = json.loads(create_response.data)['data']['id']
        
        response = client.get(f'/api/employees/{employee_id}')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['data']['first_name'] == 'John'
    
    def test_get_nonexistent_employee(self, client):
        """Test getting an employee that doesn't exist."""
        response = client.get('/api/employees/999')
        data = json.loads(response.data)
        
        assert response.status_code == 404
        assert data['success'] is False


class TestUpdateEmployee:
    """Tests for updating employees."""
    
    def test_update_employee_success(self, client, sample_employee):
        """Test successful employee update."""
        # Create an employee
        create_response = client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Update the employee
        update_data = {'first_name': 'Jane', 'department': 'HR'}
        response = client.put(
            f'/api/employees/{employee_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['data']['first_name'] == 'Jane'
        assert data['data']['department'] == 'HR'
    
    def test_update_nonexistent_employee(self, client):
        """Test updating an employee that doesn't exist."""
        response = client.put(
            '/api/employees/999',
            data=json.dumps({'first_name': 'Jane'}),
            content_type='application/json'
        )
        
        assert response.status_code == 404


class TestDeleteEmployee:
    """Tests for deleting employees."""
    
    def test_delete_employee_success(self, client, sample_employee):
        """Test successful employee deletion."""
        # Create an employee
        create_response = client.post(
            '/api/employees',
            data=json.dumps(sample_employee),
            content_type='application/json'
        )
        employee_id = json.loads(create_response.data)['data']['id']
        
        # Delete the employee
        response = client.delete(f'/api/employees/{employee_id}')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['success'] is True
        
        # Verify deletion
        get_response = client.get(f'/api/employees/{employee_id}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_employee(self, client):
        """Test deleting an employee that doesn't exist."""
        response = client.delete('/api/employees/999')
        
        assert response.status_code == 404
