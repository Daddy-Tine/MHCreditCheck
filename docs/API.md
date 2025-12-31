# API Documentation

## Base URL

All API endpoints are prefixed with `/api/v1`

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Standard Response Format

All API responses follow this format:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "meta": {}
}
```

## Endpoints

### Authentication

#### POST /api/v1/auth/register
Register a new user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "role": "BANK_USER",
  "bank_id": 1
}
```

**Response:** User object

#### POST /api/v1/auth/login
Login and get access token

**Request:** Form data
- username: email
- password: password

**Response:**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

#### POST /api/v1/auth/refresh
Refresh access token

**Request:**
```json
{
  "refresh_token": "eyJ..."
}
```

#### GET /api/v1/auth/me
Get current user information

### Users

#### GET /api/v1/users
Get list of users (Admin only)

#### POST /api/v1/users
Create a new user (Admin only)

#### GET /api/v1/users/{user_id}
Get user by ID

#### PUT /api/v1/users/{user_id}
Update user (Admin only)

#### DELETE /api/v1/users/{user_id}
Delete user (Admin only)

### Banks

#### GET /api/v1/banks
Get list of banks

#### POST /api/v1/banks
Create a new bank (Admin only)

#### GET /api/v1/banks/{bank_id}
Get bank by ID

#### PUT /api/v1/banks/{bank_id}
Update bank

#### POST /api/v1/banks/{bank_id}/approve
Approve or reject a bank (Admin only)

### Credit Data

#### POST /api/v1/credit-data
Submit credit account data

**Request:**
```json
{
  "consumer_id": 1,
  "account_number": "1234567890",
  "account_type": "CREDIT_CARD",
  "account_status": "OPEN",
  "payment_status": "CURRENT",
  "current_balance": 1000.00,
  "credit_limit": 5000.00,
  "open_date": "2020-01-01"
}
```

#### GET /api/v1/credit-data
Get credit account data

#### PUT /api/v1/credit-data/{account_id}
Update credit account data

### Credit Reports

#### POST /api/v1/credit-reports
Generate a credit report

**Request:**
```json
{
  "consumer_id": 1
}
```

**Response:** Credit report with score and account details

#### GET /api/v1/credit-reports/{report_id}
Get credit report by ID

### Inquiries

#### POST /api/v1/inquiries
Create a credit inquiry

**Request:**
```json
{
  "consumer_id": 1,
  "purpose": "LOAN_APPLICATION",
  "purpose_description": "Mortgage application"
}
```

#### GET /api/v1/inquiries
Get credit inquiries

### Disputes

#### POST /api/v1/disputes
Create a dispute

#### GET /api/v1/disputes
Get disputes

#### POST /api/v1/disputes/{dispute_id}/resolve
Resolve a dispute (Admin/Auditor only)

### Consumers

#### POST /api/v1/consumers
Create a consumer profile

#### GET /api/v1/consumers/{consumer_id}
Get consumer by ID

#### PUT /api/v1/consumers/{consumer_id}/freeze
Freeze or unfreeze consumer credit

### Audit Logs

#### GET /api/v1/audit
Get audit logs (Admin/Auditor only)

## Error Responses

Errors follow this format:

```json
{
  "success": false,
  "data": null,
  "error": {
    "detail": "Error message",
    "code": "ERROR_CODE"
  }
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting

API endpoints are rate-limited:
- 60 requests per minute per user
- 1000 requests per hour per user

## Pagination

List endpoints support pagination:
- `skip`: Number of records to skip
- `limit`: Maximum number of records to return

Example: `GET /api/v1/users?skip=0&limit=10`

