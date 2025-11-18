"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

# Example schemas (you can keep or remove if not needed)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Traffic dashboard schemas

class Transit(BaseModel):
    """
    Transit collection schema
    Collection name: "transit"
    """
    line: str = Field(..., description="Transit line identifier")
    status: str = Field(..., description="Operational status e.g., On Time, Delayed, Suspended")
    delay_minutes: int = Field(0, ge=0, description="Current delay in minutes")
    agency: Optional[str] = Field(None, description="Transit agency name")

class Accident(BaseModel):
    """
    Accident reports
    Collection name: "accident"
    """
    location: str = Field(..., description="Street and cross or area name")
    severity: str = Field(..., description="Severity level e.g., Minor, Major, Critical")
    status: str = Field("active", description="active, cleared")
    description: Optional[str] = Field(None, description="Short description")
    lat: Optional[float] = Field(None, description="Latitude")
    lng: Optional[float] = Field(None, description="Longitude")

class Roadwork(BaseModel):
    """
    Roadwork notices
    Collection name: "roadwork"
    """
    location: str = Field(..., description="Street and segment")
    impact: str = Field(..., description="Impact type e.g., Lane Closure, Full Closure, Detour")
    status: str = Field("active", description="active, scheduled, completed")
    start_date: Optional[date] = Field(None, description="Start date")
    end_date: Optional[date] = Field(None, description="End date (if known)")
    description: Optional[str] = Field(None, description="Details")
    lat: Optional[float] = Field(None, description="Latitude")
    lng: Optional[float] = Field(None, description="Longitude")

# Add your own schemas here if needed.
