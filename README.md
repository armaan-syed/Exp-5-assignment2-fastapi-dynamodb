# FastAPI CRUD API with Amazon DynamoDB

A RESTful CRUD API developed using **FastAPI** and **Amazon DynamoDB**, deployed on an **Amazon EC2 instance**. This project demonstrates how to build, deploy, and expose a backend service that performs Create, Read, Update, and Delete operations on DynamoDB.

## Project Overview

This project implements a backend API for managing items in an inventory-style system. Each item contains basic information such as its name, price, availability, tags, and additional details.

The API is deployed on an EC2 instance and communicates with DynamoDB using the EC2 instance's IAM role. AWS access keys are not stored in the application.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Amazon EC2 | Application hosting |
| Amazon DynamoDB | NoSQL database |
| Boto3 | AWS SDK for Python |
| Pydantic | Request validation and data modelling |
| Swagger UI | API testing and documentation |

## System Architecture

```text
Client / Swagger UI
        |
        v
Amazon EC2 Instance
        |
        v
FastAPI Application
        |
        v
Boto3 AWS SDK
        |
        v
EC2 IAM Role
        |
        v
Amazon DynamoDB
```

## AWS Configuration

| Configuration | Value |
|---|---|
| AWS Region | `eu-north-1` |
| DynamoDB Table | `assignment2-items` |
| Partition Key | `id` |
| Key Type | String |
| Hosting Platform | Amazon EC2 |
| Authentication | EC2 IAM Role |

## Features

- Create a new item
- Retrieve all items
- Retrieve a specific item by ID
- Update an existing item
- Delete an item
- Request validation using Pydantic
- JSON-based REST API
- Swagger UI documentation
- DynamoDB integration using Boto3
- IAM role-based AWS authentication
- Recursive conversion of numeric values for DynamoDB compatibility

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/items/{item_id}` | Create a new item |
| `GET` | `/items` | Retrieve all items |
| `GET` | `/items/{item_id}` | Retrieve one item |
| `PUT` | `/items/{item_id}` | Update an item |
| `DELETE` | `/items/{item_id}` | Delete an item |

## Item Data Model

### Create Item Request

```json
{
  "name": "Wireless Mouse",
  "price": 799,
  "available": true,
  "tags": [
    "electronics",
    "accessory"
  ],
  "details": {
    "brand": "Logitech",
    "warranty_months": 12,
    "rating": 4.5
  }
}
```

### Item Fields

| Field | Type | Description |
|---|---|---|
| `id` | String | Unique item identifier stored as the partition key |
| `name` | String | Name of the item |
| `price` | Float | Price of the item |
| `available` | Boolean | Availability status |
| `tags` | Array of strings | Item categories or tags |
| `details` | Object | Additional item metadata |

## Example API Responses

### Create Item

**Request**

```http
POST /items/item004
```

**Response**

```json
{
  "message": "Item created successfully",
  "id": "item004"
}
```

### Retrieve Item

```json
{
  "id": "item004",
  "name": "Wireless Mouse",
  "price": 799,
  "available": true,
  "tags": [
    "electronics",
    "accessory"
  ],
  "details": {
    "brand": "Logitech",
    "warranty_months": 12,
    "rating": 4.5
  }
}
```

### Update Item

**Request**

```http
PUT /items/item004
```

```json
{
  "price": 899,
  "available": false
}
```

**Response**

```json
{
  "message": "Item updated successfully",
  "id": "item004"
}
```

### Delete Item

**Request**

```http
DELETE /items/item004
```

**Response**

```json
{
  "message": "Item deleted successfully",
  "id": "item004"
}
```

## Deployment Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/assignment2-fastapi-dynamodb.git
cd assignment2-fastapi-dynamodb
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS Access

The application is designed to run on an EC2 instance with an IAM role that has permission to access the DynamoDB table.

No AWS access keys are required in the source code.

The EC2 IAM role must have permissions similar to:

- `dynamodb:PutItem`
- `dynamodb:GetItem`
- `dynamodb:Scan`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`

### 5. Start the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

```text
http://YOUR_EC2_PUBLIC_IP:8000
```

## Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open the following URL in a browser:

```text
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

The Swagger interface can be used to test all CRUD operations.

## Project Structure

```text
assignment2-fastapi-dynamodb/
│
├── main.py             # FastAPI application and CRUD logic
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore          # Ignored files and folders
└── venv/               # Local virtual environment, not committed
```

## Security Considerations

- AWS credentials are not hardcoded in the application.
- DynamoDB access is performed using an EC2 IAM role.
- The virtual environment is excluded from Git.
- Environment files and sensitive credentials are excluded using `.gitignore`.
- IAM permissions should follow the principle of least privilege.

## Testing Checklist

- [x] EC2 instance configured
- [x] DynamoDB table created
- [x] IAM role attached to EC2
- [x] FastAPI application deployed
- [x] Create operation tested successfully
- [ ] Read all items tested
- [ ] Read single item tested
- [ ] Update operation tested
- [ ] Delete operation tested

## Author

**Armaan Syed**

Computer Engineering  
Fr. Conceicao Rodrigues College of Engineering, Mumbai
