1. Aim

To develop and deploy a RESTful CRUD API using FastAPI and Amazon DynamoDB on an Amazon EC2 instance, using an EC2 IAM role for secure database access.

2. Objectives

Create and configure a DynamoDB table.

Demonstrate at least five DynamoDB attribute types.

Implement Create, Read, Update, and Delete operations.

Deploy the FastAPI application on EC2.

Access DynamoDB using IAM role-based authentication.

Test the API using Swagger UI.

3. Technologies Used

Python, FastAPI, Uvicorn, Boto3, Amazon EC2, Amazon DynamoDB, Pydantic, and Swagger UI.

4. System Architecture
Client / Swagger UI
        ↓
Amazon EC2
        ↓
FastAPI Application
        ↓
Boto3 SDK
        ↓
EC2 IAM Role
        ↓
Amazon DynamoDB
5. AWS Configuration

Configuration

	

Value




EC2 Instance

	

mealie-lab4




DynamoDB Table

	

assignment2-items




AWS Region

	

eu-north-1




Partition Key

	

id




Key Type

	

HASH




Key Data Type

	

String (S)




Billing Mode

	

PAY_PER_REQUEST




API Port

	

8000

6. DynamoDB Table Creation

The table was created using Python and Boto3.

import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="eu-north-1"
)

table = dynamodb.create_table(
    TableName="assignment2-items",
    KeySchema=[
        {
            "AttributeName": "id",
            "KeyType": "HASH"
        }
    ],
    AttributeDefinitions=[
        {
            "AttributeName": "id",
            "AttributeType": "S"
        }
    ],
    BillingMode="PAY_PER_REQUEST"
)

table.wait_until_exists()
print("Table created successfully!")

Table: assignment2-items Partition Key: id Type: String (S)

7. DynamoDB Attribute Types

The application demonstrates the following DynamoDB attribute types:

Attribute

	

Example

	

Type




id

	

"item004"

	

String (S)




name

	

"Wireless Mouse"

	

String (S)




price

	

799

	

Number (N)




available

	

true

	

Boolean (BOOL)




tags

	

["electronics", "accessory"]

	

List (L)




details

	

{"brand": "Logitech"}

	

Map (M)

Sample Item JSON
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

Proof: Attach a DynamoDB Console screenshot showing the assignment2-items table and the stored item004 record.

8. API Endpoints

Method

	

Endpoint

	

Description




POST

	

/items/{item_id}

	

Create an item




GET

	

/items

	

Retrieve all items




GET

	

/items/{item_id}

	

Retrieve one item




PUT

	

/items/{item_id}

	

Update an item




DELETE

	

/items/{item_id}

	

Delete an item

Sample Request — Create
POST /items/item004
{
  "name": "Wireless Mouse",
  "price": 799,
  "available": true,
  "tags": ["electronics", "accessory"],
  "details": {
    "brand": "Logitech",
    "warranty_months": 12,
    "rating": 4.5
  }
}
Sample Response
{
  "message": "Item created successfully",
  "id": "item004"
}
9. Deployment and Testing

The application was deployed on the EC2 instance using the following commands:

cd ~/assignment2
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

Swagger UI was accessed at:

http://16.171.24.173:8000/docs
CRUD Testing Summary

Operation

	

Endpoint

	

Result




Create

	

POST /items/item004

	

Item created successfully




Read All

	

GET /items

	

Items retrieved




Read One

	

GET /items/item004

	

Item details retrieved




Update

	

PUT /items/item004

	

Item updated successfully




Delete

	

DELETE /items/item004

	

Item deleted successfully

For update testing, the following request can be used:

{
  "price": 899,
  "available": false
}

After deletion, requesting GET /items/item004 returns:

{
  "detail": "Item not found"
}
Screenshots to Include

DynamoDB table showing assignment2-items and partition key id.

DynamoDB item showing the five attribute types.

Swagger UI showing the CRUD endpoints.

Successful POST response showing 200 OK.

GET, PUT, and DELETE operation results.

GitHub repository showing the source code.

10. IAM Security

The EC2 instance uses the IAM role:

EC2-DynamoDB-Assignment2-Role

The role allows the application to perform DynamoDB operations such as:

dynamodb:PutItem
dynamodb:GetItem
dynamodb:Scan
dynamodb:UpdateItem
dynamodb:DeleteItem

No AWS access keys are hardcoded in the application. Boto3 automatically obtains permissions through the EC2 IAM role.

11. GitHub Repository

The project source code and documentation are available at:

https://github.com/armaan-syed/Exp-5-assignment2-fastapi-dynamodb 

Repository files:

main.py
README.md
requirements.txt
.gitignore
12. Result

A FastAPI CRUD application was successfully deployed on Amazon EC2 and integrated with Amazon DynamoDB. The application successfully created and managed inventory items using REST API endpoints.

The implementation demonstrated the following DynamoDB attribute types:

String (S)

Number (N)

Boolean (BOOL)

List (L)

Map (M)

13. Conclusion

This experiment demonstrated the practical implementation of a NoSQL cloud database application using Amazon DynamoDB. FastAPI was used to develop the REST API, EC2 was used for deployment, and an IAM role provided secure access to DynamoDB without storing AWS credentials in the code.