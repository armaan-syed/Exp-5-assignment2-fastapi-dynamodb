from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from decimal import Decimal
import boto3
from botocore.exceptions import ClientError


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Assignment 2 - DynamoDB CRUD API",
    description="CRUD application using FastAPI and DynamoDB",
    version="1.0.0"
)


# --------------------------------------------------
# DynamoDB configuration
# --------------------------------------------------

AWS_REGION = "eu-north-1"
TABLE_NAME = "assignment2-items"

# Boto3 automatically uses the IAM Role attached
# to the EC2 instance.
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table(TABLE_NAME)


# --------------------------------------------------
# Convert Python values to DynamoDB-safe values
# --------------------------------------------------

def to_decimal(value):
    """
    DynamoDB does not support Python float values.
    Convert all floats and integers to Decimal.
    Preserve Boolean values as Boolean.
    Handle nested dictionaries and lists.
    """

    if isinstance(value, bool):
        return value

    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, int):
        return Decimal(str(value))

    if isinstance(value, Decimal):
        return value

    if isinstance(value, dict):
        return {
            str(key): to_decimal(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            to_decimal(item)
            for item in value
        ]

    return value


# --------------------------------------------------
# Convert DynamoDB Decimal values to JSON-safe values
# --------------------------------------------------

def from_decimal(value):
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)

    if isinstance(value, dict):
        return {
            key: from_decimal(val)
            for key, val in value.items()
        }

    if isinstance(value, list):
        return [
            from_decimal(item)
            for item in value
        ]

    return value


# --------------------------------------------------
# Request models
# --------------------------------------------------

class Item(BaseModel):
    name: str
    price: float
    available: bool
    tags: List[str]
    details: Dict[str, Any]


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    tags: Optional[List[str]] = None
    details: Optional[Dict[str, Any]] = None


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Assignment 2 API is running",
        "database": "DynamoDB",
        "table": TABLE_NAME,
        "partition_key": "id",
        "authentication": "EC2 IAM Role"
    }


# --------------------------------------------------
# CREATE
# --------------------------------------------------

@app.post("/items/{item_id}")
def create_item(item_id: str, item: Item):
    try:
        item_data = item.model_dump()

        # Match the actual DynamoDB partition key.
        item_data["id"] = item_id

        # Convert all numeric values before writing.
        item_data = to_decimal(item_data)

        table.put_item(
            Item=item_data,
            ConditionExpression="attribute_not_exists(id)"
        )

        return {
            "message": "Item created successfully",
            "id": item_id
        }

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "ConditionalCheckFailedException":
            raise HTTPException(
                status_code=409,
                detail="Item with this ID already exists"
            )

        raise HTTPException(
            status_code=500,
            detail=f"DynamoDB error: {str(error)}"
        )


# --------------------------------------------------
# READ ALL
# --------------------------------------------------

@app.get("/items")
def get_all_items():
    try:
        response = table.scan()

        items = [
            from_decimal(item)
            for item in response.get("Items", [])
        ]

        return {
            "count": len(items),
            "items": items
        }

    except ClientError as error:
        raise HTTPException(
            status_code=500,
            detail=f"DynamoDB error: {str(error)}"
        )


# --------------------------------------------------
# READ ONE
# --------------------------------------------------

@app.get("/items/{item_id}")
def get_item(item_id: str):
    try:
        response = table.get_item(
            Key={
                "id": item_id
            }
        )

        if "Item" not in response:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return from_decimal(response["Item"])

    except ClientError as error:
        raise HTTPException(
            status_code=500,
            detail=f"DynamoDB error: {str(error)}"
        )


# --------------------------------------------------
# UPDATE
# --------------------------------------------------

@app.put("/items/{item_id}")
def update_item(item_id: str, item: UpdateItem):
    update_fields = item.model_dump(exclude_unset=True)

    if not update_fields:
        raise HTTPException(
            status_code=400,
            detail="Provide at least one field to update"
        )

    # Convert floats and nested numeric values.
    update_fields = to_decimal(update_fields)

    expression_parts = []
    expression_names = {}
    expression_values = {}

    for field, value in update_fields.items():
        expression_parts.append(f"#{field} = :{field}")
        expression_names[f"#{field}"] = field
        expression_values[f":{field}"] = value

    try:
        response = table.update_item(
            Key={
                "id": item_id
            },
            UpdateExpression="SET " + ", ".join(expression_parts),
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )

        return {
            "message": "Item updated successfully",
            "item": from_decimal(response["Attributes"])
        }

    except ClientError as error:
        raise HTTPException(
            status_code=500,
            detail=f"DynamoDB error: {str(error)}"
        )


# --------------------------------------------------
# DELETE
# --------------------------------------------------

@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    try:
        response = table.delete_item(
            Key={
                "id": item_id
            },
            ReturnValues="ALL_OLD"
        )

        if "Attributes" not in response:
            raise HTTPException(
                status_code=404,
                detail="Item not found"
            )

        return {
            "message": "Item deleted successfully",
            "deleted_item": from_decimal(
                response["Attributes"]
            )
        }

    except ClientError as error:
        raise HTTPException(
            status_code=500,
            detail=f"DynamoDB error: {str(error)}"
        )
