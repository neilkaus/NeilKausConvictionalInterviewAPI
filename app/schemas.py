# schemas.py
# file contains all the schemas (implemented as pydantic models) used by FastAPI to specificy models
# for output/input to functions to their verify validity, fill in default values and create documentation

from pydantic import BaseModel, Field
from typing import List, Optional

class error(BaseModel):
    message: str

class image(BaseModel):
    source: str
    variantId: str = Field(description="ID for the variant the image relates to")

class weight(BaseModel):
    value: Optional[int] = None
    unit: Optional[str] = None

class variant(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    sku: Optional[str] = None
    available: Optional[bool] = Field( False, description="True if inventory > 0, false otherwise")
    inventory_quantity: Optional[int] = Field(0, description="Inventory for given variant. Should be 0 if no information provided")
    variantWeight: Optional[weight] = Field(None, alias="weight")

class inventory(BaseModel):
    productId: Optional[str] = None
    variantId: Optional[str] = None
    stock:  Optional[int] = None

class product(BaseModel):
    code: str
    title: Optional[str] = None
    vendor: Optional[str] = None
    bodyHtml: Optional[str] = None
    variants: Optional[List[variant]] = None
    images: Optional[List[image]] = None
